# Generated by Django 4.1.5 on 2023-04-26 08:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nebenet_app', '0013_user_date_alter_ticket_ti_personal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='pro_salenumber',
            field=models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
