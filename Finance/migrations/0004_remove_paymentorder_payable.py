# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0003_paymentorder_payable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentorder',
            name='payable',
        ),
    ]
