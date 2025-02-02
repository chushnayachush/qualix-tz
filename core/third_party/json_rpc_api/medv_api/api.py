import json
import typing

from core.third_party.json_rpc_api.base import JSONRpcAPIBase
from core.third_party.json_rpc_api.entities import (
    RequestBody,
    Response,
    ResponseAPIErrorBody,
    ResponseBody,
    ResponseErrorBody,
)


class API(JSONRpcAPIBase):
    @typing.override
    def make_api_call(
        self,
        request_body: RequestBody,
        *args: tuple[typing.Any, ...],
        headers: dict[str, str | int] | None = None,
        **kwargs: dict[str, typing.Any],
    ) -> Response:
        try:
            response = self._requests.post_request(
                url=self.api_url,
                json=request_body.as_dict(),
                headers=headers or {},
            )
        except self._requests.possible_exceptions as e:
            return Response(
                status_code=400,
                body=ResponseAPIErrorBody(
                    id=request_body.id,
                    method=request_body.method,
                    server_error=str(e),
                ),
            )

        response_json_body = json.loads(response.body)
        error = response_json_body.get("error", "")

        if error:
            response_body = ResponseErrorBody(
                id=response_json_body.get("id", ""),
                method=response_json_body.get("method", ""),
                error=error,
            )
        else:
            result = response_json_body.get("result", "")
            response_body = ResponseBody(
                id=response_json_body.get("id", ""),
                method=response_json_body.get("method", ""),
                result=result,
            )

        return Response(status_code=response.status_code, body=response_body)
