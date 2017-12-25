from django.db import models


class Driver(models.Model):
    name = models.CharField(null=False, verbose_name='司机姓名', max_length=256)
    identity_number = models.CharField(verbose_name='身份证号', max_length=256)
    birthday = models.DateField(verbose_name='出生日期', null=False)
    license = models.CharField(null=False, verbose_name='驾照号', max_length=256)


class DispatchRecord(models.Model):
    vehicle_number = models.CharField(null=False, verbose_name='车牌号', max_length=30)
    dispatch_date = models. DateField(null=False, verbose_name='发车日期')
    origin = models.CharField(null=False, verbose_name='发出地', max_length=256)
    destination = models.CharField(null=False, verbose_name='到达地', max_length=256)
    comments = models.CharField(null=True, verbose_name='备注', max_length=800)
