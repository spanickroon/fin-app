from django.contrib import admin

from apps.logs.models import SystemLog
from django_otp.plugins.otp_totp.models import TOTPDevice


class SystemLogAdmin(admin.ModelAdmin):
    model = SystemLog
    can_add = False
    can_change = False
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

class TOTPDeviceAdmin(admin.ModelAdmin):
    model = TOTPDevice
    can_add = False
    can_change = False
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(SystemLog, SystemLogAdmin)
admin.site.unregister(TOTPDevice)
admin.site.register(TOTPDevice, TOTPDeviceAdmin)

