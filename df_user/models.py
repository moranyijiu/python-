# coding=utf-8

from django.db import models


# 构建用户模型
class UserInfo(models.Model):
    # u'***'修改的是后台展示信息的名字字段
    uname = models.CharField(u'用户名', max_length=20)
    # 密码采用暗文，sha1加密转换为40字节
    upwd = models.CharField(u'密码', max_length=40)
    uemail = models.CharField(u'电子邮箱', max_length=30)
    ushow = models.CharField(u'收件人名字', max_length=20, default='')
    uaddress = models.CharField(u'收件地址', max_length=100, default='')
    uyoubian = models.CharField(u'收件邮编', max_length=6, default='')
    uphone = models.CharField(u'收件人电话', max_length=11, default='')

    # default,blank是python层面的约束,不影响数据库表结构

    # 用户对象名字返回，后台订单管理现实
    def __str__(self):
        return self.uname.encode('utf-8')

    # 修改后台管理界面显示
    class Meta:
        verbose_name_plural = '用户管理'

