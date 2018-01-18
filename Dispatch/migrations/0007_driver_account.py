# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Dispatch', '0006_auto_20180117_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='account',
            field=models.ForeignKey(verbose_name='司机账户', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
