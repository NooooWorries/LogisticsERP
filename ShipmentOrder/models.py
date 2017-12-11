from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user_id = models.ForeignKey(User, verbose_name='用户ID')
    gender = models.BooleanField(verbose_name='性别')
    birthday = models.DateTimeField(null=True, verbose_name='生日')
    role = models.IntegerField(null=0, verbose_name='角色')


class CustomerClass(models.Model):
    class_name = models.CharField(null=False, verbose_name='类名', max_length=256)
    comments = models.CharField(null=False, verbose_name='备注', max_length=256)


class Customer(models.Model):
    customer_class = models.ForeignKey(CustomerClass)
    customer_name = models.CharField(null=False, verbose_name='客户名', max_length=256)
    contact_person = models.CharField(null=False, verbose_name='联系人', max_length=256)
    contact_number = models.CharField(null=False, verbose_name='联系电话', max_length=256)
    identity_number = models.CharField(null=False, verbose_name='身份证号码', max_length=18)
    gender = models.BooleanField(verbose_name='性别')
    address = models.CharField(null=False, verbose_name='地址', max_length=18)
    comments = models.CharField(verbose_name='备注', max_length=18)
    payable = models.FloatField(default=0, verbose_name='应收余额')


class ShipmentOrder(models.Model):
    #发货人信息
    sender = models.CharField(null=False, verbose_name='发货人', max_length=256)
    from_address = models.CharField(null=False, verbose_name='发出地地址', max_length=256)
    sender_contact = models.CharField(null=False, verbose_name='发货人联系电话', max_length=256)

    #收货人信息
    receiver = models.CharField(null=False, verbose_name='收货人', max_length=256)
    to_address = models.CharField(null=False, verbose_name='到达地地址', max_length=256)
    receiver_contact = models.CharField(null=False, verbose_name='收货人联系电话', max_length=256)

    #费用
    collectFee = models.FloatField(default=0, verbose_name='接货费')
    sendFee = models.FloatField(default=0, verbose_name='送货费')
    paymentOnAccountFreight = models.FloatField(default=0, verbose_name='垫付运费')
    transitFee = models.FloatField(default=0, verbose_name='中转费')
    installFee = models.FloatField(default=0, verbose_name='装卸费')
    storeFee = models.FloatField(default=0, verbose_name='保管费')
    insuranceFee = models.FloatField(default=0, verbose_name='保价费')
    freight = models.FloatField(default=0, verbose_name='运费')
    packingFee = models.FloatField(default=0, verbose_name='包装费')
    totalPrice = models.FloatField(default=0, verbose_name='总价')

    #其他
    mode = models.CharField(null=False, verbose_name='运输方式', max_length=256)
    comments = models.CharField(verbose_name='备注', max_length=256)
    status = models.IntegerField(null=False, default=0, verbose_name="状态")  # 0:草稿， 1:待审核， 2:审核通过， 3:审核不通过


class Goods(models.Model):
    shipment_order_id = models.ForeignKey(ShipmentOrder)
    goods_name = models.CharField(null=False, verbose_name='货物名称', max_length=256)
    amount = models.FloatField(null=False, default=1, verbose_name='数量')
    volume = models.FloatField(null=False, verbose_name='体积')
    weight = models.FloatField(null=False, verbose_name='重量')
    freight = models.FloatField(null=False, verbose_name='运费')
    claim_value = models.FloatField(null=False, verbose_name='申明价值')
    insurance_rate = models.FloatField(null=False, default=1, verbose_name='保价率')
    insurance_fee = models.FloatField(null=False, default=0, verbose_name='保价费')


class BankAccount(models.Model):
    account_name = models.CharField(null=False, verbose_name='账号名', max_length=256)
    bank = models.CharField(null=False, verbose_name='开户银行', max_length=256)
    account_number = models.IntegerField(null=False, verbose_name='账号')
    card_holder = models.CharField(null=False, verbose_name='持卡人', max_length=256)


class Payment(models.Model):
    summary = models.CharField(null=False, verbose_name='摘要', max_length=1024)
    customer = models.ForeignKey(Customer, verbose_name='客户')
    amount = models.FloatField(null=False, verbose_name='支付金额')
    time = models.DateTimeField(null=False, verbose_name='制单时间')
    handle = models.ForeignKey(User, verbose_name='经办')


class PaymentOrder(models.Model):
    payment_id = models.ForeignKey(Payment, verbose_name='付款账单')
    order = models.ForeignKey(ShipmentOrder, verbose_name='运送单')
