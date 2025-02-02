from django.urls import path, URLPattern

from request_sender.views import send_api_request_apiview, send_api_request_templateview

urlpatterns = [
    path("send_request/", send_api_request_apiview, name="send_api_request"),
    path("", send_api_request_templateview, name="index"),
]
