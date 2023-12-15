from django.urls import path

from apps.documents.views import DocumentVerificationView

urlpatterns = [
    path(
        "document_verification/",
        DocumentVerificationView.as_view(),
        name="document_verification",
    ),
]
