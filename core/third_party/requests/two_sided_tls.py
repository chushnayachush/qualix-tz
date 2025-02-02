import ssl
import socket
import typing
import http.client
from urllib.parse import urlparse
from tempfile import NamedTemporaryFile

import json as jsonlib

from core.utils.http import https_connection
from core.third_party.requests.base import RequestsBase
from core.third_party.requests.entities import Response
from core.utils.types import CAPath, Certfile, Keyfile, KeyfilePassword


class TLSProtectedRequester(RequestsBase):
    class InvalidHostnameError(ValueError, BaseException): ...

    class ConnectionTimedOutError(ValueError, BaseException): ...

    class HTTPError(ValueError, BaseException): ...

    class ServerIssue(ValueError, BaseException): ...

    possible_exceptions: tuple[type[Exception], ...] = (
        InvalidHostnameError,
        ConnectionTimedOutError,
        HTTPError,
        ServerIssue,
    )

    def __init__(
        self,
        cert_file: Certfile,
        key_file: Keyfile,
        ca_path: CAPath,
        keyfile_pass: KeyfilePassword | None = None,
        default_headers: dict[str, str | int] | None = None,
    ) -> None:
        self._cert: Certfile = cert_file
        self._key: Keyfile = key_file
        self._keyfile_pass: KeyfilePassword | None = keyfile_pass
        self._capath: CAPath = ca_path
        self._context: ssl.SSLContext = ssl.SSLContext(
            protocol=ssl.PROTOCOL_TLS_CLIENT
        )
        self._default_headers: dict[str, str | int] = default_headers or {}
        self._fill_ssl_context()

    def _fill_ssl_context(self) -> None:
        # INFO: https://github.com/python/cpython/issues/60691
        with (
            NamedTemporaryFile(mode="w+b") as certfile,
            NamedTemporaryFile(mode="w+b") as keyfile,
        ):
            _ = certfile.write(self._cert.encode())
            _ = certfile.seek(0)

            _ = keyfile.write(self._key.encode())
            _ = keyfile.seek(0)

            self._context.load_cert_chain(
                certfile=certfile.name,
                keyfile=keyfile.name,
                password=self._keyfile_pass,
            )
        self._context.load_verify_locations(capath=self._capath)

    def _request(
        self,
        method: str,
        url: str,
        port: int,
        body: str | None = None,
        json: dict[str, typing.Hashable] | str | None = None,
        headers: dict[str, str | int] | None = None,
    ) -> Response | typing.NoReturn:
        # INFO: Берем общие заголовки для класса и объединяем их с теми, что передали конкретно в запрос.
        # INFO: Приоритет у заголовков запроса в случае накладки.
        headers = dict(self._default_headers)
        headers.update(headers or {})

        # INFO: json рассматриваем как тело, в приоритете то, что дали в json, если ничего не дали берем body
        if json:
            body = jsonlib.dumps(json) if not isinstance(json, str) else json

        parsed_url = urlparse(url)
        if parsed_url.hostname:
            with https_connection(
                url=parsed_url.hostname, port=port, ctx=self._context
            ) as conn:
                print(f"trying to {method} {url} with body={body}")
                try:
                    conn.request(
                        method=method,
                        url=parsed_url.path,
                        body=body,
                        headers=headers,
                    )
                except socket.gaierror:
                    raise TLSProtectedRequester.InvalidHostnameError(
                        "Invalid api hostname."
                    )

                except socket.timeout:
                    raise TLSProtectedRequester.ConnectionTimedOutError(
                        "Failed to establish a connection to api."
                    )

                except http.client.HTTPException as e:
                    raise TLSProtectedRequester.HTTPError(
                        f"Error with HTTP, more context: {str(e)}"
                    )

                except Exception as e:
                    print(e)
                    raise TLSProtectedRequester.ServerIssue(
                        "Server issues occured. Please try again later, we already know about this."
                    )

                response = conn.getresponse()
                return Response(
                    status_code=response.status,
                    reason=response.reason,
                    body=response.read().decode(),
                )

        raise TLSProtectedRequester.InvalidHostnameError(
            "Invalid api hostname."
        )

    @typing.override
    def post_request(
        self,
        url: str,
        body: str | None = None,
        port: int = 443,
        headers: dict[str, str | int] | None = None,
        json: dict[str, typing.Hashable] | str | None = None,
        *args: tuple[typing.Any, ...],
        **kwargs: dict[str, typing.Any],
    ) -> Response:
        return self._request(
            method="POST",
            url=url,
            port=port,
            body=body,
            json=json,
            headers=headers or {},
        )

    @typing.override
    def get_request(
        self,
        url: str,
        *args: tuple[typing.Any, ...],
        **kwargs: dict[str, typing.Any],
    ) -> Response:
        raise NotImplementedError

    @typing.override
    def put_request(
        self,
        url: str,
        *args: tuple[typing.Any, ...],
        **kwargs: dict[str, typing.Any],
    ) -> Response:
        raise NotImplementedError

    @typing.override
    def patch_request(
        self,
        url: str,
        *args: tuple[typing.Any, ...],
        **kwargs: dict[str, typing.Any],
    ) -> Response:
        raise NotImplementedError

    @typing.override
    def delete_request(
        self,
        url: str,
        *args: tuple[typing.Any, ...],
        **kwargs: dict[str, typing.Any],
    ) -> Response:
        raise NotImplementedError
