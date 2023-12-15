# Generated by Django 4.2.6 on 2023-11-23 15:14

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("categories", "0001_initial"),
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                ("name", models.CharField()),
                ("code", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "rate",
                    models.DecimalField(decimal_places=2, default=1, max_digits=10),
                ),
                ("is_prev_amount", models.BooleanField(default=False)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="categories.category",
                    ),
                ),
            ],
            options={
                "db_table": "payments",
            },
        ),
        migrations.CreateModel(
            name="PaymentTemplate",
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
                ("name", models.CharField()),
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
                "db_table": "payment_templates",
            },
        ),
        migrations.CreateModel(
            name="PaymentHistory",
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
                ("payment_time", models.DateTimeField(auto_now_add=True)),
                (
                    "prev_amount",
                    models.IntegerField(blank=True, default=None, null=True),
                ),
                ("current_amount", models.IntegerField(default=0)),
                (
                    "price_amount",
                    models.DecimalField(decimal_places=2, default=1, max_digits=10),
                ),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="categories.category",
                    ),
                ),
                (
                    "payment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="payments.payment",
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="payments",
                        to="payments.paymenttemplate",
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
                "db_table": "payment_history",
            },
        ),
    ]