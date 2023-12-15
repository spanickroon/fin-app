from django.urls import path

from apps.payments.views import (PaymentsHistoryView, PaymentsTemplateView,
                                 PaymentsView, PaymentView)

urlpatterns = [
    path("", PaymentsView.as_view(), name="payments"),
    path("<int:category_id>", PaymentsView.as_view(), name="payment_by_category"),
    path(
        "<int:category_id>/<int:payment_id>",
        PaymentView.as_view(),
        name="payment_by_id",
    ),
    path("history/", PaymentsHistoryView.as_view(), name="history"),
    path("templates/", PaymentsTemplateView.as_view(), name="templates"),
    path("templates/<int:template>", PaymentsTemplateView.as_view(), name="template"),
]
