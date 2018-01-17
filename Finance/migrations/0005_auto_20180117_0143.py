# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0004_remove_paymentorder_payable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentorder',
            name='shipment_order',
            field=models.ForeignKey(verbose_name='订单', on_delete=models.SET('订单被删除'), to='ShipmentOrder.ShipmentOrder'),
        ),
    ]
