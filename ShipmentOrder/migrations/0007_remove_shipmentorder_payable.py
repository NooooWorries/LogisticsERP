# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShipmentOrder', '0006_shipmentorder_payable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipmentorder',
            name='payable',
        ),
    ]
