from django.db import models

from apps.authentication.models import UserProfile
from django.utils.translation import gettext_lazy as _


class SystemLog(models.Model):
    userprofile = models.ForeignKey(
        UserProfile, verbose_name=_("User Profile"), null=True, blank=True, on_delete=models.DO_NOTHING
    )
    log_time = models.DateTimeField(verbose_name=_("Log time"), auto_now_add=True, blank=True)
    action = models.CharField(verbose_name=_("Action"))

    def __str__(self) -> str:
        return f"{self.userprofile.user.username}: {self.log_time}; {self.action}"

    class Meta:
        db_table = "system_logs"
        verbose_name = _("System log")
        verbose_name_plural = _("System logs")
