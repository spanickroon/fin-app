# Generated by Django 4.2.6 on 2023-11-23 15:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("authentication", "0001_initial"),
        ("documents", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CreditRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "request_amount",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "approved_amount",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                (
                    "document",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="documents.document",
                    ),
                ),
                (
                    "userprofile",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="authentication.userprofile",
                    ),
                ),
            ],
            options={
                "db_table": "credit_requests",
            },
        ),
    ]