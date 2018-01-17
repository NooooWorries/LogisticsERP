# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0002_paymentorder_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentorder',
            name='payable',
            field=models.FloatField(verbose_name='剩余应付', default=0),
        ),
    ]
