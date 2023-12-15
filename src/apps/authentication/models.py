from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    USER = "user"
    MODERATOR = "moderator"

    ROLES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
    )

    user = models.OneToOneField(
        User, verbose_name=_('User'), on_delete=models.CASCADE, null=False, related_name="profile"
    )
    role = models.CharField(choices=ROLES, verbose_name=_('Role'), default=USER)

    def __str__(self) -> str:
        return f"{self.user.username}"

    class Meta:
        db_table = "user_profiles"
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

