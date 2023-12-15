from django.urls import path

from apps.base.views import BaseView

urlpatterns = [
    path("", BaseView.as_view(), name="base"),
]
