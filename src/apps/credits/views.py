import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.credits.forms import CreditForm
from apps.credits.services import credit_service


class CreditView(LoginRequiredMixin, View):
    login_url = "login"
    redirect_field_name = "redirect_to"

    def get(self, request: HttpResponse, *args, **kwargs) -> HttpResponse:
        return render(request, template_name="credits/base.html")

    def post(self, request: HttpResponse, *args, **kwargs) -> HttpResponse:
        service_result = credit_service.execute(request, CreditForm(request.POST))
        logging.info(f"{self.__class__} {service_result}")
        
        if service_result == service_result.BAD_REQUEST:
            context = {'error': 'Неправильная форма или нет документов ДУЛ'}
        else:
            context = {}
        
        return render(request, template_name="credits/base.html", context=context)
