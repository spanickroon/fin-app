import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.documents.forms import DocumentForm
from apps.documents.services import document_service


class DocumentVerificationView(LoginRequiredMixin, View):
    login_url = "login"
    redirect_field_name = "redirect_to"

    def get(self, request: HttpResponse, *args, **kwargs) -> HttpResponse:
        return render(request, template_name="documents/base.html")

    def post(self, request: HttpResponse, *args, **kwargs) -> HttpResponse:
        service_result = document_service.execute(
            request, DocumentForm(request.POST, request.FILES)
        )
        logging.info(f"{self.__class__} {service_result}")

        if service_result == service_result.BAD_REQUEST:
            context = {'error': 'Кривой документ'}
        else:
            context = {}

        return render(request, template_name="documents/base.html", context=context)
