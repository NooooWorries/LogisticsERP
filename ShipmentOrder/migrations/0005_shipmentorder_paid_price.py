# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShipmentOrder', '0004_auto_20180105_0259'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipmentorder',
            name='paid_price',
            field=models.FloatField(verbose_name='已支付款项', default=0),
        ),
    ]
