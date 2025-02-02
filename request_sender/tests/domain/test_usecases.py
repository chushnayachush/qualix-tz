from unittest import mock

from core.third_party.json_rpc_api.entities import (
    Response,
    ResponseBody,
    RequestBody,
)
from core.utils.testutils import UnitTestCase

from request_sender.domain.usecases import SendJSONRpcApiRequestUsecase


class SendJSONRpcApiRequestUsecaseUnitTestCase(UnitTestCase):
    def test_execute__calls_api__and_returns(
        self,
    ):
        api_mock = mock.MagicMock()
        api_mock.make_api_call.return_value = Response(
            status_code=200,
            body=ResponseBody(
                id="test-id",
                method="test-method",
                result="test_result",
            ),
        )

        usecase = SendJSONRpcApiRequestUsecase(json_rpc_api=api_mock)
        res = usecase.execute({"id": 1, "method": "method", "params": []})

        api_mock.make_api_call.assert_called_once_with(
            request_body=RequestBody(id="1", method="method", params=[])
        )
        assert res is api_mock.make_api_call.return_value
