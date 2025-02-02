from unittest import mock

from django.test import override_settings
from django.test.testcases import SimpleTestCase

from core.third_party.json_rpc_api import medv_api
from core.third_party.requests import two_sided_tls
from core.utils.testutils import UnitTestCase, HeavyTestCase

from request_sender.domain.factories import (
    get_send_medv_json_rpc_api_request_usecase,
)
from request_sender.domain.usecases import SendJSONRpcApiRequestUsecase


@override_settings(
    MEDV_API_CERT="",
    MEDV_API_KEY="",
    CA_PATH="/",
)
class FactoriesUnitTestCase(SimpleTestCase):
    @mock.patch(
        "core.third_party.requests.two_sided_tls.TLSProtectedRequester._fill_ssl_context"
    )
    def test__get_send_medv_json_rpc_api_request_usecase__returns_correctly_setup_usecase(
        self,
        fill_ssl_mock: mock.Mock,
    ):
        fill_ssl_mock.return_value = None
        usecase = get_send_medv_json_rpc_api_request_usecase()
        self.assertIsInstance(usecase, SendJSONRpcApiRequestUsecase)
        self.assertIsInstance(usecase._api, medv_api.API)
        self.assertIsInstance(
            usecase._api._requests, two_sided_tls.TLSProtectedRequester
        )
        fill_ssl_mock.assert_called_once()
