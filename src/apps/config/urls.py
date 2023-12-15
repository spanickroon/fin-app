from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("", RedirectView.as_view(url="base"), name="index"),
    path("admin/", admin.site.urls),
    path("base/", include("apps.base.urls")),
    path("auth/", include("apps.authentication.urls")),
    path("categories/", include("apps.categories.urls")),
    path("documents/", include("apps.documents.urls")),
    path("credits/", include("apps.credits.urls")),
    path("payments/", include("apps.payments.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
