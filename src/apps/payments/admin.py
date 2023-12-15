from django.contrib import admin

from apps.payments.models import Payment, PaymentHistory


class PaymentHistoryAdmin(admin.ModelAdmin):
    model = PaymentHistory
    can_add = False
    can_change = False
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(PaymentHistory, PaymentHistoryAdmin)
admin.site.register(Payment)