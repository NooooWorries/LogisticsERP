from django.db import models
from django.contrib.auth.models import User
from Customers import models as customer_model
from Dispatch import models as dispatch_model

class ShipmentOrder(models.Model):
    # 客户
    customer = models.ForeignKey(customer_model.Customer, null=True, on_delete=models.SET_NULL)

    # 发货人信息
    sender = models.CharField(null=False, verbose_name='发货人', max_length=256)
    from_address = models.CharField(null=False, verbose_name='发出地地址', max_length=256)
    sender_contact = models.CharField(null=False, verbose_name='发货人联系电话', max_length=256)

    # 收货人信息
    receiver = models.CharField(null=False, verbose_name='收货人', max_length=256)
    to_address = models.CharField(null=False, verbose_name='到达地地址', max_length=256)
    receiver_contact = models.CharField(null=False, verbose_name='收货人联系电话', max_length=256)

    # 费用
    paymentOnAccountFreight = models.FloatField(default=0, verbose_name='垫付运费')
    claimed_value = models.FloatField(null=False, default=0, verbose_name='声明价值')
    insurance_rate = models.FloatField(null=False, default=1, verbose_name='保价率')
    insurance_fee = models.FloatField(null=False, default=0, verbose_name='保价费')
    freight = models.FloatField(default=0, verbose_name='运费')
    packingFee = models.FloatField(default=0, verbose_name='包装费')
    totalPrice = models.FloatField(default=0, verbose_name='总价')
    paid_price = models.FloatField(null=False, default=0, verbose_name="已支付款项")
    payable = models.FloatField(null=False, default=0, verbose_name="应付款项")

    # 其他
    mode = models.CharField(null=False, verbose_name='运输方式', max_length=256)
    volume = models.FloatField(null=False, verbose_name='体积', default=0)
    density = models.FloatField(null=False, verbose_name='密度', default=0)
    comments = models.CharField(verbose_name='备注', max_length=256)
    create_date = models.DateField(verbose_name='创建时间', null=False)
    handle = models.ForeignKey(User, null=False, verbose_name='经办')
    market = models.CharField(verbose_name='市场', max_length=200, null=True)
    status = models.IntegerField(null=False, default=0, verbose_name="状态")  # 0:未提交， 1:待审核， 2:审核通过， 3:已完成

    class Meta:
        verbose_name = "运送订单"


class Goods(models.Model):
    shipment_order_id = models.ForeignKey(ShipmentOrder)
    pack_number = models.IntegerField(null=False, default=1, verbose_name="包号")
    goods_name = models.CharField(null=False, verbose_name='货物名称', max_length=256)

    # 数据
    amount = models.FloatField(null=False, default=0, verbose_name='数量')
    unit_price = models.FloatField(null=False,verbose_name='运费单价')
    weight = models.FloatField(null=False, verbose_name='重量')
    volume = models.FloatField(null=False, verbose_name='体积', default=0)
    freight = models.FloatField(null=False, verbose_name='运费')
    density = models.FloatField(null=False, default=0, verbose_name='密度')

    # 日期
    store_date = models.DateField(verbose_name='入库日期', null=True)
    send_date = models.DateField(verbose_name='发货日期', null=True)
    receive_date = models.DateField(verbose_name='到达日期', null=True)

    # 出车
    status = models.IntegerField(null=False, default=0, verbose_name="状态")  # 0：入库，1：装车，2：口岸，3：到达
    dispatch = models.ForeignKey(dispatch_model.DispatchRecord, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "货物"
