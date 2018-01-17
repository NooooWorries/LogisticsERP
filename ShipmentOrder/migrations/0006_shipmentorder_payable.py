# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShipmentOrder', '0005_shipmentorder_paid_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipmentorder',
            name='payable',
            field=models.FloatField(verbose_name='待支付款项', default=0.0),
        ),
    ]
