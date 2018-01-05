# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShipmentOrder', '0003_remove_goods_barcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='density',
            field=models.FloatField(verbose_name='密度', default=0),
        ),
        migrations.AddField(
            model_name='goods',
            name='volume',
            field=models.FloatField(verbose_name='体积', default=0),
        ),
    ]
