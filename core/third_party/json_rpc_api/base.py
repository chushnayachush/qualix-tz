from abc import ABC
import typing

from .entities import RequestBody, Response

from core.third_party.requests.base import RequestsBase


class JSONRpcAPIBase(ABC):
    def __init__(self, requests: RequestsBase, api_url: str) -> None:
        self._requests: RequestsBase = requests

        self.api_url: str = api_url

    def make_api_call(
        self,
        request_body: RequestBody,
        *args: tuple[typing.Any, ...],
        **kwargs: dict[str, typing.Any],
    ) -> Response: ...
