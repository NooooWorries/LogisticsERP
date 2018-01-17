# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dispatch', '0005_driver_comments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dispatchrecord',
            options={'verbose_name': '出车记录'},
        ),
        migrations.AlterModelOptions(
            name='driver',
            options={'verbose_name': '司机'},
        ),
    ]
