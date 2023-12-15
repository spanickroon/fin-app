from django.urls import path

from apps.credits.views import CreditView

urlpatterns = [
    path("make_credit/", CreditView.as_view(), name="make_credit"),
]
