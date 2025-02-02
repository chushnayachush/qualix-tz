import typing

from core.third_party.json_rpc_api.entities import Response, RequestBody
from core.third_party.json_rpc_api.base import JSONRpcAPIBase


class SendJSONRpcApiRequestUsecase:
    def __init__(self, json_rpc_api: JSONRpcAPIBase) -> None:
        self._api: JSONRpcAPIBase = json_rpc_api

    def execute(self, form_data: dict[str, typing.Any]) -> Response:
        return self._api.make_api_call(
            request_body=RequestBody(
                id=str(form_data.get("id", "")),
                method=form_data.get("method", ""),
                params=form_data.get("params", ""),
            )
        )
