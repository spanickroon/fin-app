import json
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views import View

from apps.categories.services import category_service


class CategoriesView(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "redirect_to"

    def get(self, request: HttpResponse, *args, **kwargs) -> HttpResponse:
        service_result = category_service.execute()
        logging.info(
            f"{self.__class__} {json.dumps(service_result, indent=4, ensure_ascii=False).encode('utf-8').decode()}"
        )
        return render(
            request,
            template_name="categories/base.html",
            context={"categories": service_result},
        )
