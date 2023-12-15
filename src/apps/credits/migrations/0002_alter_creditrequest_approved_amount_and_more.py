# Generated by Django 4.2.6 on 2023-11-23 18:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("credits", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="creditrequest",
            name="approved_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=None,
                max_digits=10,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.AlterField(
            model_name="creditrequest",
            name="request_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                default=None,
                max_digits=10,
                null=True,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
    ]