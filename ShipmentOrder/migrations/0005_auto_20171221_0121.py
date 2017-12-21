# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-21 01:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShipmentOrder', '0004_auto_20171220_0813'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shipmentorder',
            old_name='insuranceFee',
            new_name='insurance_fee',
        ),
        migrations.AddField(
            model_name='shipmentorder',
            name='claimed_value',
            field=models.FloatField(default=0, verbose_name='声明价值'),
        ),
    ]
