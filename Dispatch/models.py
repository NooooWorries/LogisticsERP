from django.db import models


class Driver(models.Model):
    name = models.CharField(null=False, verbose_name='司机姓名', max_length=256)
    identity_number = models.CharField(verbose_name='身份证号', max_length=256)
    birthday = models.DateField(verbose_name='出生日期', null=False)
    license = models.CharField(null=False, verbose_name='驾照号', max_length=256)
    comments = models.CharField(null=True, verbose_name='备注', max_length=800)

    class Meta:
        verbose_name = "司机"


class DispatchRecord(models.Model):
    driver = models.ForeignKey(Driver, null=True, on_delete=models.SET_NULL)
    vehicle_number = models.CharField(null=False, verbose_name='车牌号', max_length=30)
    dispatch_date = models.DateField(null=False, verbose_name='发车日期')
    origin = models.CharField(null=False, verbose_name='发出地', max_length=256)
    destination = models.CharField(null=False, verbose_name='到达地', max_length=256)
    comments = models.CharField(null=True, verbose_name='备注', max_length=800)
    status = models.IntegerField(null=False, verbose_name='状态', default=0)  # 0:草稿, 1:提交, 2:送达

    class Meta:
        verbose_name = "出车记录"
