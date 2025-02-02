from django.conf import settings

from core.utils.types import CAPath, Certfile, Keyfile
from core.third_party.requests.two_sided_tls import TLSProtectedRequester
from core.third_party.json_rpc_api.medv_api import API as MedvAPI

from request_sender.domain.usecases import SendJSONRpcApiRequestUsecase


def get_send_medv_json_rpc_api_request_usecase() -> (
    SendJSONRpcApiRequestUsecase
):
    return SendJSONRpcApiRequestUsecase(
        json_rpc_api=MedvAPI(
            requests=TLSProtectedRequester(
                cert_file=Certfile(settings.MEDV_API_CERT),
                key_file=Keyfile(settings.MEDV_API_KEY),
                ca_path=CAPath(settings.CA_PATH),
                default_headers={"Content-Type": "application/json"},
            ),
            api_url=settings.MEDV_API_URL,
        )
    )
