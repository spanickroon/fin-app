from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    parent_category = models.ForeignKey(
        "self",
        verbose_name=_('Parent Category'),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children_category",
    )
    name = models.CharField(verbose_name=_('Name'), max_length=100)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        db_table = "categories"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
