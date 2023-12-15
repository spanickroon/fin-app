from django.urls import path

from apps.categories.views import CategoriesView

urlpatterns = [
    path("all/", CategoriesView.as_view(), name="category"),
]
