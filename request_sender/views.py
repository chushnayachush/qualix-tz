import json
import typing

from django import views
from django import forms
from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from request_sender.domain.usecases import SendJSONRpcApiRequestUsecase
from request_sender.domain.factories import (
    get_send_medv_json_rpc_api_request_usecase,
)


@typing.final
class SendAPIRequestSerializer(forms.Form):
    id = forms.CharField(min_length=1, required=True)
    method = forms.CharField(min_length=1, required=True)
    params = forms.JSONField(required=False)


@method_decorator(csrf_exempt, name="dispatch")
class SendAPIRequestAPIView(views.View):
    _usecase: SendJSONRpcApiRequestUsecase = (
        get_send_medv_json_rpc_api_request_usecase()
    )
    _serializer: type[SendAPIRequestSerializer] = SendAPIRequestSerializer

    def post(self, request: HttpRequest) -> JsonResponse:
        # по идее здесь должен быть какой-нибудь сериализатор
        try:
            form_data = json.loads(request.body.decode())
        except json.JSONDecodeError:
            return JsonResponse(
                status=400, data={"message": "Provide valid json."}
            )

        serializer = self._serializer(form_data)
        if not serializer.is_valid():
            return JsonResponse(status=400, data={"message": serializer.errors})

        response = self._usecase.execute(form_data=serializer.data).as_dict()
        return JsonResponse(status=200, data=response)


class SendAPIRequestTemplateView(TemplateView):
    template_name = "form.html"


send_api_request_apiview = SendAPIRequestAPIView.as_view()
send_api_request_templateview = SendAPIRequestTemplateView.as_view()
