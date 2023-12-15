from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.authentication.models import UserProfile
from apps.documents.models import Document


class CreditRequest(models.Model):
    userprofile = models.ForeignKey(
        UserProfile, verbose_name=_('User Profile'), null=True, blank=True, on_delete=models.DO_NOTHING
    )
    document = models.ForeignKey(
        Document, verbose_name=_("Document"), null=True, blank=True, on_delete=models.DO_NOTHING
    )
    request_amount = models.DecimalField(
        verbose_name=_("Request amount"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        default=None,
        validators=[MinValueValidator(0)],
    )

    approved_amount = models.DecimalField(
        verbose_name=_("Approved amount"),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        default=None,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        db_table = "credit_requests"
        verbose_name = _("Credit")
        verbose_name_plural = _("Credits")