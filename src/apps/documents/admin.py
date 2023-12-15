from django.contrib import admin

from apps.documents.models import Document


class DocumentAdmin(admin.ModelAdmin):
    model = Document
    can_add = False
    can_change = False
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Document, DocumentAdmin)