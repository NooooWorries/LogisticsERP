# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShipmentOrder', '0007_remove_shipmentorder_payable'),
    ]

    operations = [
        migrations.AddField(
            model_name='shipmentorder',
            name='payable',
            field=models.FloatField(verbose_name='应付款项', default=0),
        ),
    ]
