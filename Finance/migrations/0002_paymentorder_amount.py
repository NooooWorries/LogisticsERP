# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentorder',
            name='amount',
            field=models.FloatField(verbose_name='付款金额', default=0),
            preserve_default=False,
        ),
    ]
