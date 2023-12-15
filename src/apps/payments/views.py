import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.payments.forms import PaymentForm
from apps.payments.services import payment_service


class PaymentsView(LoginRequiredMixin, View):
    login_url = "login"
    redirect_field_name = "redirect_to"

    def get(self, request: HttpResponse, *args, **kwargs) -> HttpResponse:
        service_result = (
            payment_service.execute(
                request,
                action=payment_service.get_payment_action,
                payment_data=None,
                **kwargs,
            )
            if kwargs
            else payment_service.execute(
                request,
                action=payment_service.get_all_payments_action,
                payment_data=None,
            )
        )
        logging.info(f"{self.__class__} {service_result}")

        return render(
            request,
            template_name="payments/base.html",
            context={"payments": service_result},
        )


class PaymentView(LoginRequiredMixin, View):
    login_url = "login"
    redirect_field_name = "redirect_to"

    def get(self, request: HttpResponse, *args, **kwargs) -> HttpResponse:
        service_result = payment_service.execute(
            request,
            action=payment_service.get_payment_action,
            payment_data=None,
            **kwargs,
        )
        logging.info(f"{self.__class__} {service_result}")

        return render(
            request,
            template_name="payments/payment.html",
            context={"payment": service_result},
        )

    def post(self, request: HttpResponse, *args, **kwargs) -> HttpResponse:
        service_result = payment_service.execute(
            request,
            action=payment_service.make_payment_action,
            payment_data=PaymentForm(request.POST),
            **kwargs,
        )
        logging.info(f"{self.__class__} {service_result}")

        return render(
            request,
            template_name="payments/payment.html",
            context={"qr_code": service_result},
        )


class PaymentsHistoryView(LoginRequiredMixin, View):
    login_url = "login"
    redirect_field_name = "redirect_to"

    def get(self, request: HttpResponse, *args, **kwargs) -> HttpResponse:
        service_result = payment_service.execute(
            request,
            action=payment_service.get_history,
            payment_data=None,
            **kwargs,
        )
        logging.info(f"{self.__class__} {service_result}")
        return render(
            request,
            template_name="payments/history.html",
            context={"history": service_result},
        )


class PaymentsTemplateView(LoginRequiredMixin, View):
    login_url = "login"
    redirect_field_name = "redirect_to"

    def get(self, request: HttpResponse, *args, **kwargs) -> HttpResponse:
        return render(request, template_name="payments/base.html")

    def post(self, request: HttpResponse, *args, **kwargs) -> HttpResponse:
        return render(request, template_name="payments/base.html")
