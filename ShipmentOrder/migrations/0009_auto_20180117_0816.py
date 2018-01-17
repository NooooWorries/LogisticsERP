# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShipmentOrder', '0008_shipmentorder_payable'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'verbose_name': '货物'},
        ),
        migrations.AlterModelOptions(
            name='shipmentorder',
            options={'verbose_name': '运送订单'},
        ),
    ]
