import uuid

from django.db import models

from apps.authentication.models import UserProfile
from apps.categories.models import Category
from django.utils.translation import gettext_lazy as _


class PaymentTemplate(models.Model):
    userprofile = models.ForeignKey(
        UserProfile, verbose_name=_("User Profile"), null=True, blank=True, on_delete=models.DO_NOTHING
    )
    name = models.CharField(verbose_name=_("Name"))

    def __str__(self) -> str:
        return f"{self.userprofile.user.username}: {self.name}"

    class Meta:
        db_table = "payment_templates"
        verbose_name = _("Payment template")
        verbose_name_plural = _("Payment templates")


class Payment(models.Model):
    category = models.ForeignKey(
        Category, verbose_name=_("Category"), null=False, blank=False, on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name=_("Name"), max_length=100)
    code = models.UUIDField(verbose_name=_("Code"), default=uuid.uuid4, editable=False)
    rate = models.DecimalField(
        verbose_name=_("Rate"), null=False, blank=False, default=1, decimal_places=2, max_digits=10
    )
    is_prev_amount = models.BooleanField(verbose_name=_("Prev Amount"), null=False, blank=False, default=False)

    def __str__(self) -> str:
        return f"{self.category}: {self.name}"

    class Meta:
        db_table = "payments"
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")


class PaymentHistory(models.Model):
    userprofile = models.ForeignKey(
        UserProfile, verbose_name=_("User Profile"), null=True, blank=True, on_delete=models.DO_NOTHING
    )
    payment = models.ForeignKey(
        Payment, verbose_name=_("Payment"), null=True, blank=True, on_delete=models.DO_NOTHING
    )
    template = models.ForeignKey(
        PaymentTemplate,
        verbose_name=_("Payment template"),
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="payments",
    )
    category = models.ForeignKey(
        Category, verbose_name=_("Category"), null=True, blank=True, on_delete=models.DO_NOTHING
    )
    payment_time = models.DateTimeField(verbose_name=_("Payment time"), auto_now_add=True, blank=True)
    prev_amount = models.DecimalField(
        verbose_name=_("Prev amount"), null=True, blank=True, default=None, decimal_places=2, max_digits=10
    )
    current_amount = models.DecimalField(
        verbose_name=_("Payment time"), null=False, blank=False, default=0, decimal_places=2, max_digits=10
    )
    price_amount = models.DecimalField(
        verbose_name=_("Price amount"), null=False, blank=False, default=1, decimal_places=2, max_digits=10
    )

    def __str__(self) -> str:
        return f"{self.userprofile.user.username}: {self.category}; {self.payment_time}"

    class Meta:
        db_table = "payment_history"
        verbose_name = _("Payment history")
        verbose_name_plural = _("Payment histories")
