from django.db import models
from ShipmentOrder.models import ShipmentOrder
from django.contrib.auth.models import User


class PaymentOrder(models.Model):
    shipment_order = models.ForeignKey(ShipmentOrder, null=False, on_delete=models.SET("订单被删除"), verbose_name='订单')
    payment_date = models.DateField(null=False, verbose_name='支付日期')
    amount = models.FloatField(null=False, verbose_name='付款金额')
    comments = models.CharField(null=True, verbose_name='备注', max_length=800)
    handle = models.ForeignKey(User, null=False, verbose_name='经办')

    class Meta:
        verbose_name = "收款记录"
