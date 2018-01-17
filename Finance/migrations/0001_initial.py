# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ShipmentOrder', '0005_shipmentorder_paid_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('payment_date', models.DateField(verbose_name='支付日期')),
                ('comments', models.CharField(verbose_name='备注', max_length=800, null=True)),
                ('handle', models.ForeignKey(verbose_name='经办', to=settings.AUTH_USER_MODEL)),
                ('shipment_order', models.ForeignKey(on_delete=models.SET('订单被删除'), to='ShipmentOrder.ShipmentOrder')),
            ],
        ),
    ]
