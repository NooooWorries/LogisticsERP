from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, verbose_name="用户")
    # 0: 管理员
    # 1: 入库员
    # 2: 文员
    # 3: 司机
    # 4: 财务
    role = models.IntegerField(verbose_name='角色', null=False)
    gender = models.BooleanField(verbose_name='性别')
    birthday = models.DateTimeField(null=True, verbose_name='生日')
    comments = models.CharField(null=True, verbose_name='备注', max_length=500)

    class Meta:
        verbose_name = '用户资料'

