# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-26 06:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShipmentOrder', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='barcode',
            field=models.FloatField(max_length=1024, null=True, verbose_name='条码路径'),
        ),
    ]