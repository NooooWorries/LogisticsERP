from django.db import models


# Create your models here.
class CustomerClass(models.Model):
    class_name = models.CharField(null=False, verbose_name='类名', max_length=256)
    comments = models.CharField(null=False, verbose_name='备注', max_length=256)


class Customer(models.Model):
    customer_class = models.ForeignKey(CustomerClass, null=True, on_delete=models.SET_NULL)
    customer_name = models.CharField(null=False, verbose_name='客户名', max_length=256)
    contact_person = models.CharField(null=False, verbose_name='联系人', max_length=256)
    contact_number = models.CharField(null=False, verbose_name='联系电话', max_length=256)
    identity_number = models.CharField(null=True, verbose_name='身份证号码', max_length=18)
    gender = models.BooleanField(verbose_name='性别')
    address = models.CharField(null=False, verbose_name='地址', max_length=256)
    comments = models.CharField(verbose_name='备注', max_length=18)
    payable = models.FloatField(default=0, verbose_name='应收余额')