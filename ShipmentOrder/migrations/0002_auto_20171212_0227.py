# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-12 02:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShipmentOrder', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipmentorder',
            name='handle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='经办'),
        ),
    ]