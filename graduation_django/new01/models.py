from django.db import models
from django.contrib.auth.models import User
# Create your models here.



from django.db import models

class YourModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='姓名')
    age = models.IntegerField(verbose_name='年龄')

    def __str__(self):
        return self.name

class BjHouse(models.Model):
    id = models.AutoField(primary_key=True)
    jianjie = models.CharField(max_length=100, null=True, verbose_name='简介')
    xiaoqu = models.CharField(max_length=100, null=True, verbose_name='小区')
    huxing = models.CharField(max_length=100, null=True, verbose_name='户型')
    mianji = models.FloatField(null=True, verbose_name='面积')
    guanzhurenshu = models.IntegerField(null=True, verbose_name='关注人数')
    guankancishu = models.IntegerField(null=True, verbose_name='观看次数')
    fabushijian = models.CharField(max_length=100, null=True, verbose_name='发布时间')
    fangjia = models.FloatField(null=True, verbose_name='房价')
    danjia = models.IntegerField(null=True, verbose_name='单价/平')
    chengqu = models.CharField(max_length=100, null=True, verbose_name='城区')
    jingdu = models.FloatField(null=True, verbose_name='经度')
    weidu = models.FloatField(null=True, verbose_name='纬度')

    def __str__(self):
        return self.xiaoqu


class UserViewHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(BjHouse, on_delete=models.CASCADE)
    view_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-view_time']  # 按浏览时间倒序排列
