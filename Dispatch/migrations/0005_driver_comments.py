# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dispatch', '0004_dispatchrecord_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='comments',
            field=models.CharField(verbose_name='备注', max_length=800, null=True),
        ),
    ]
