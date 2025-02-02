import typing
from dataclasses import dataclass

from core.utils.dataclasses import FrozenPatchedDataclass


@dataclass(frozen=True)
class RequestBase(FrozenPatchedDataclass):
    id: str
    method: str


@dataclass(frozen=True)
class RequestBody(RequestBase):
    params: list[typing.Any] | dict[str, typing.Hashable] | None = None
    jsonrpc: str = "2.0"


@dataclass(frozen=True)
class ResponseBody(RequestBase):
    result: typing.Any


@dataclass(frozen=True)
class ResponseErrorBody(RequestBase):
    error: typing.Any


@dataclass(frozen=True)
class ResponseAPIErrorBody(RequestBase):
    server_error: typing.Any


@dataclass(frozen=True)
class Response(FrozenPatchedDataclass):
    body: ResponseBody | ResponseErrorBody | ResponseAPIErrorBody
    status_code: int
