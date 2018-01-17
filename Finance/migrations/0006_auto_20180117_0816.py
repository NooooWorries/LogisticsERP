# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0005_auto_20180117_0143'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='paymentorder',
            options={'verbose_name': '收款记录'},
        ),
    ]
