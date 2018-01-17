# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customer',
            options={'verbose_name': '客户'},
        ),
        migrations.AlterModelOptions(
            name='customerclass',
            options={'verbose_name': '客户组'},
        ),
    ]
