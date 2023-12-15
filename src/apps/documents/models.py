from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.authentication.models import UserProfile


class Document(models.Model):
    userprofile = models.ForeignKey(
        UserProfile, verbose_name=_("User Profile"), null=True, blank=True, on_delete=models.DO_NOTHING
    )
    document_photo = models.ImageField(verbose_name=_("Document photo"), upload_to="documents/")
    birth_date = models.DateField(verbose_name=_("Birth Date"), default=None, blank=True, null=True)
    country = models.CharField(verbose_name=_("Country"), default=None, blank=True, null=True, max_length=100)
    id_number = models.CharField(verbose_name=_("Id number"), default=None, blank=True, null=True, max_length=20)

    def __str__(self) -> str:
        return f"{self.userprofile.user.username}: {self.id_number}"

    class Meta:
        db_table = "documents"
        verbose_name = _("Document")
        verbose_name_plural = _("Documents")