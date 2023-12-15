from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class BaseView(LoginRequiredMixin, View):
    login_url = "login"
    redirect_field_name = "redirect_to"

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpRequest:
        return render(request, template_name="base/base.html")
