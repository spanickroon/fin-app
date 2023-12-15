import logging

from django.contrib import messages

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from http import HTTPStatus

from apps.authentication.forms import AuthUserForm, OTPAuthUserForm
from apps.authentication.services import (
    login_user_service,
    logout_user_service,
    registration_user_service,
)


class LoginView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, template_name="authentication/login.html")

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        service_result = login_user_service.execute(request, OTPAuthUserForm(request.POST))
        logging.info(f'{self.__class__} {service_result}')

        messages.success(request, service_result.message)

        if service_result.status == HTTPStatus.OK:
            return redirect('base')

        return render(request, template_name='authentication/login.html', context={**service_result.dict()})


class RegistrationView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        return render(request, template_name="authentication/registration.html")

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        service_result = registration_user_service.execute(
            request, AuthUserForm(request.POST)
        )
        logging.info(f"{self.__class__} {service_result}")

        messages.success(request, service_result.message)

        return render(
            request,
            template_name="authentication/registration.html",
            context={**service_result.dict()},
        )


class LogoutView(View):

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        service_result = logout_user_service.execute(request).dict()
        logging.info(f"{self.__class__} {service_result}")
        return redirect("base")
