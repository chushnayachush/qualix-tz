import json
from unittest import mock

from core.utils.testutils import UnitTestCase

from core.third_party.requests.two_sided_tls import TLSProtectedRequester
from core.third_party.requests.entities import Response as RawResponse
from core.third_party.json_rpc_api.entities import (
    RequestBody,
    Response,
    ResponseAPIErrorBody,
    ResponseBody,
    ResponseErrorBody,
)
from core.third_party.json_rpc_api.medv_api import API as MedvAPI


class TestMedvAPIUnitTestCase(UnitTestCase):
    def test__correct_call__no_side_effects__result_present__constructs_response(
        self,
    ):
        requests_mock = mock.MagicMock()
        requests_mock.post_request.return_value = RawResponse(
            status_code=200,
            reason="",
            body=json.dumps(
                {"id": "test-id", "method": "test-method", "result": 123}
            ),
        )
        api = MedvAPI(
            requests=requests_mock,
            api_url="api_url",
        )
        request_body = RequestBody(
            id="test-id",
            method="test-method",
        )

        response = api.make_api_call(request_body=request_body)

        requests_mock.post_request.assert_called_once_with(
            url=api.api_url,
            json=request_body.as_dict(),
            headers={},
        )
        assert response.status_code == 200
        self.assertIsInstance(response.body, ResponseBody)
        assert response.body.id == "test-id"
        assert response.body.method == "test-method"
        assert response.body.result == 123

    def test__correct_call__no_side_effects__error_present__constructs_response(
        self,
    ):
        requests_mock = mock.MagicMock()
        requests_mock.post_request.return_value = RawResponse(
            status_code=200,
            reason="",
            body=json.dumps(
                {"id": "test-id", "method": "test-method", "error": 123}
            ),
        )
        api = MedvAPI(
            requests=requests_mock,
            api_url="api_url",
        )
        request_body = RequestBody(
            id="test-id",
            method="test-method",
        )

        response = api.make_api_call(request_body=request_body)

        requests_mock.post_request.assert_called_once_with(
            url=api.api_url,
            json=request_body.as_dict(),
            headers={},
        )
        assert response.status_code == 200
        self.assertIsInstance(response.body, ResponseErrorBody)
        assert response.body.id == "test-id"
        assert response.body.method == "test-method"
        assert response.body.error == 123

    def test__correct_call__side_effects__constructs_response(
        self,
    ):
        requests_mock = mock.MagicMock()
        requests_mock.possible_exceptions = (
            *TLSProtectedRequester.possible_exceptions,
        )

        api = MedvAPI(
            requests=requests_mock,
            api_url="api_url",
        )
        request_body = RequestBody(
            id="test-id",
            method="test-method",
        )

        expected_calls = []
        for possible_side_effect in TLSProtectedRequester.possible_exceptions:
            requests_mock.post_request.side_effect = possible_side_effect(
                possible_side_effect.__name__
            )

            response = api.make_api_call(request_body=request_body)

            expected_calls.append(
                mock.call(
                    url=api.api_url,
                    json=request_body.as_dict(),
                    headers={},
                )
            )
            assert response.status_code == 400
            self.assertIsInstance(response.body, ResponseAPIErrorBody)
            assert response.body.server_error == str(
                possible_side_effect(possible_side_effect.__name__)
            )

        requests_mock.post_request.assert_has_calls(expected_calls)
