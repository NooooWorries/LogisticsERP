# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-22 01:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Dispatch', '0001_initial'),
        ('ShipmentOrder', '0007_auto_20171221_0616'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_id',
        ),
        migrations.AddField(
            model_name='goods',
            name='dispatch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Dispatch.DispatchRecord'),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
