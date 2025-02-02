import http.client
import socket
import tempfile
from pathlib import Path
from unittest import mock

from core.utils.testutils import UnitTestCase

from core.third_party.requests.base import Response as RawResponse
from core.third_party.requests.two_sided_tls import TLSProtectedRequester
from core.utils.types import CAPath, Certfile, Keyfile, KeyfilePassword


class TLSProtectedRequesterUnitTestCase(UnitTestCase):
    @mock.patch("core.third_party.requests.two_sided_tls.NamedTemporaryFile")
    @mock.patch("ssl.SSLContext")
    def test_fill_ssl_context(
        self, mock_ssl_context, mock_named_temporary_file
    ):
        cert = "dummy_cert"
        key = "dummy_key"
        keyfile_pass = "dummy_password"
        capath = Path("/dummy/capath")
        mock_certfile = mock.MagicMock()
        mock_keyfile = mock.MagicMock()
        mock_certfile.name = "/tmp/certfile"
        mock_keyfile.name = "/tmp/keyfile"
        mock_named_temporary_file.side_effect = [
            mock.MagicMock(
                __enter__=mock.MagicMock(return_value=mock_certfile)
            ),
            mock.MagicMock(__enter__=mock.MagicMock(return_value=mock_keyfile)),
        ]
        mock_context_instance = mock.MagicMock()
        mock_ssl_context.return_value = mock_context_instance

        instance = TLSProtectedRequester(
            cert_file=Certfile(cert),
            key_file=Keyfile(key),
            keyfile_pass=KeyfilePassword(keyfile_pass),
            ca_path=CAPath(capath),
        )
        assert mock_named_temporary_file.call_count == 2
        mock_certfile.write.assert_called_once_with(cert.encode())
        mock_certfile.seek.assert_called_once_with(0)
        mock_keyfile.write.assert_called_once_with(key.encode())
        mock_keyfile.seek.assert_called_once_with(0)
        mock_context_instance.load_cert_chain.assert_called_once_with(
            certfile=mock_certfile.name,
            keyfile=mock_keyfile.name,
            password=keyfile_pass,
        )
        mock_context_instance.load_verify_locations.assert_called_once_with(
            capath=capath,
        )

    @mock.patch("core.third_party.requests.two_sided_tls.NamedTemporaryFile")
    @mock.patch("ssl.SSLContext")
    def test__not_implemented_methods(
        self, mock_ssl_context, mock_named_temporary_file
    ):
        cert = "dummy_cert"
        key = "dummy_key"
        keyfile_pass = "dummy_password"
        capath = Path("/dummy/capath")
        mock_certfile = mock.MagicMock()
        mock_keyfile = mock.MagicMock()
        mock_certfile.name = "/tmp/certfile"
        mock_keyfile.name = "/tmp/keyfile"
        mock_named_temporary_file.side_effect = [
            mock.MagicMock(
                __enter__=mock.MagicMock(return_value=mock_certfile)
            ),
            mock.MagicMock(__enter__=mock.MagicMock(return_value=mock_keyfile)),
        ]
        mock_context_instance = mock.MagicMock()
        mock_ssl_context.return_value = mock_context_instance

        instance = TLSProtectedRequester(
            cert_file=Certfile(cert),
            key_file=Keyfile(key),
            keyfile_pass=KeyfilePassword(keyfile_pass),
            ca_path=CAPath(capath),
        )

        methods = (
            "get_request",
            "patch_request",
            "put_request",
            "delete_request",
        )
        for method in methods:
            with self.assertRaises(NotImplementedError):
                getattr(instance, method)("askdjaslkjdlsakjdksjak")

    @mock.patch("core.third_party.requests.two_sided_tls.NamedTemporaryFile")
    @mock.patch("ssl.SSLContext")
    @mock.patch(
        "core.third_party.requests.two_sided_tls.TLSProtectedRequester._request"
    )
    def test__post_request__proxy__request__when_no_side_effects(
        self, _request_mock, mock_ssl_context, mock_named_temporary_file
    ):
        cert = "dummy_cert"
        key = "dummy_key"
        keyfile_pass = "dummy_password"
        capath = Path("/dummy/capath")
        mock_certfile = mock.MagicMock()
        mock_keyfile = mock.MagicMock()
        mock_certfile.name = "/tmp/certfile"
        mock_keyfile.name = "/tmp/keyfile"
        mock_named_temporary_file.side_effect = [
            mock.MagicMock(
                __enter__=mock.MagicMock(return_value=mock_certfile)
            ),
            mock.MagicMock(__enter__=mock.MagicMock(return_value=mock_keyfile)),
        ]
        mock_context_instance = mock.MagicMock()
        mock_ssl_context.return_value = mock_context_instance
        _request_mock.return_value = RawResponse(
            status_code=200, reason="test-reason", body="asdasdasdasdasdas"
        )

        instance = TLSProtectedRequester(
            cert_file=Certfile(cert),
            key_file=Keyfile(key),
            keyfile_pass=KeyfilePassword(keyfile_pass),
            ca_path=CAPath(capath),
        )
        result = instance.post_request(url="asldkaslkdjlkasjkdas", body="{}")

        _request_mock.assert_called_once_with(
            method="POST",
            url="asldkaslkdjlkasjkdas",
            body="{}",
            port=443,
            json=None,
            headers={},
        )
        assert result.status_code == 200
        assert result.reason == "test-reason"
        assert result.body == "asdasdasdasdasdas"

    @mock.patch("core.third_party.requests.two_sided_tls.NamedTemporaryFile")
    @mock.patch("ssl.SSLContext")
    def test__incorrect_api_url__no_hostname(
        self, mock_ssl_context, mock_named_temporary_file
    ):
        cert = "dummy_cert"
        key = "dummy_key"
        keyfile_pass = "dummy_password"
        capath = Path("/dummy/capath")
        mock_certfile = mock.MagicMock()
        mock_keyfile = mock.MagicMock()
        mock_certfile.name = "/tmp/certfile"
        mock_keyfile.name = "/tmp/keyfile"
        mock_named_temporary_file.side_effect = [
            mock.MagicMock(
                __enter__=mock.MagicMock(return_value=mock_certfile)
            ),
            mock.MagicMock(__enter__=mock.MagicMock(return_value=mock_keyfile)),
        ]
        mock_context_instance = mock.MagicMock()
        mock_ssl_context.return_value = mock_context_instance

        instance = TLSProtectedRequester(
            cert_file=Certfile(cert),
            key_file=Keyfile(key),
            keyfile_pass=KeyfilePassword(keyfile_pass),
            ca_path=CAPath(capath),
        )

        with self.assertRaises(TLSProtectedRequester.InvalidHostnameError):
            result = instance.post_request(url="/", body="{}")

    @mock.patch("core.third_party.requests.two_sided_tls.https_connection")
    @mock.patch("core.third_party.requests.two_sided_tls.NamedTemporaryFile")
    @mock.patch("ssl.SSLContext")
    def test__correct__call__returns_response__no_side_effect(
        self,
        mock_ssl_context,
        mock_named_temporary_file,
        mock_http_connection_context,
    ):
        cert = "dummy_cert"
        key = "dummy_key"
        keyfile_pass = "dummy_password"
        capath = Path("/dummy/capath")
        mock_certfile = mock.MagicMock()
        mock_keyfile = mock.MagicMock()
        mock_certfile.name = "/tmp/certfile"
        mock_keyfile.name = "/tmp/keyfile"
        mock_named_temporary_file.side_effect = [
            mock.MagicMock(
                __enter__=mock.MagicMock(return_value=mock_certfile)
            ),
            mock.MagicMock(__enter__=mock.MagicMock(return_value=mock_keyfile)),
        ]
        mock_named_temporary_file.return_value
        mock_context_instance = mock.MagicMock()
        mock_ssl_context.return_value = mock_context_instance
        mocked_http_connection = mock.MagicMock()
        mock_http_connection_context.return_value.__enter__.return_value = (
            mocked_http_connection
        )
        mocked_http_connection_response = mock.MagicMock()
        mocked_http_connection.getresponse.return_value = (
            mocked_http_connection_response
        )

        mocked_http_connection_response.status = 200
        mocked_http_connection_response.reason = "reason"
        mocked_http_connection_response.read.return_value = b"asdf"

        instance = TLSProtectedRequester(
            cert_file=Certfile(cert),
            key_file=Keyfile(key),
            keyfile_pass=KeyfilePassword(keyfile_pass),
            ca_path=CAPath(capath),
        )

        response = instance._request(
            method="test-method", url="htts://google.com", port=443
        )

        assert response.status_code == 200
        assert response.reason == "reason"
        assert response.body == "asdf"

    @mock.patch("core.third_party.requests.two_sided_tls.https_connection")
    @mock.patch("core.third_party.requests.two_sided_tls.NamedTemporaryFile")
    @mock.patch("ssl.SSLContext")
    def test__correct_call__reraises_exc__from__known(
        self,
        mock_ssl_context,
        mock_named_temporary_file,
        mock_http_connection_context,
    ):
        cert = "dummy_cert"
        key = "dummy_key"
        keyfile_pass = "dummy_password"
        capath = Path("/dummy/capath")
        mock_certfile = mock.MagicMock()
        mock_keyfile = mock.MagicMock()
        mock_certfile.name = "/tmp/certfile"
        mock_keyfile.name = "/tmp/keyfile"
        mock_named_temporary_file.side_effect = [
            mock.MagicMock(
                __enter__=mock.MagicMock(return_value=mock_certfile)
            ),
            mock.MagicMock(__enter__=mock.MagicMock(return_value=mock_keyfile)),
        ]
        mock_named_temporary_file.return_value
        mock_context_instance = mock.MagicMock()
        mock_ssl_context.return_value = mock_context_instance
        mocked_http_connection = mock.MagicMock()
        mock_http_connection_context.return_value.__enter__.return_value = (
            mocked_http_connection
        )
        known_exc_mapping = {
            socket.gaierror: TLSProtectedRequester.InvalidHostnameError,
            socket.timeout: TLSProtectedRequester.ConnectionTimedOutError,
            http.client.HTTPException: TLSProtectedRequester.HTTPError,
            Exception: TLSProtectedRequester.ServerIssue,
        }
        instance = TLSProtectedRequester(
            cert_file=Certfile(cert),
            key_file=Keyfile(key),
            keyfile_pass=KeyfilePassword(keyfile_pass),
            ca_path=CAPath(capath),
        )
        for raised, reraised in known_exc_mapping.items():
            mocked_http_connection.request.side_effect = raised
            with self.assertRaises(reraised):
                instance._request(
                    method="test-method", url="htts://google.com", port=443
                )
