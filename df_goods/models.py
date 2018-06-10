#coding=utf-8

from django.db import models
from tinymce.models import HTMLField

# 商品类型模型
class TypeInfo(models.Model):
    # u'***'是在后台注册时替换属性名字
    ttitle=models.CharField(u'种类',max_length=20)
    isDelete=models.BooleanField(default=False)
    # 商品类型对象返回名字
    def __str__(self):
        return self.ttitle.encode('utf-8')
    class Meta:
        verbose_name_plural = '水果类型修改'

# 商品模型
class GoodsInfo(models.Model):
    gtitle=models.CharField(u'名字',max_length=20)
    gpic=models.ImageField(u'图片',upload_to='df_goods')
    gprice=models.DecimalField(u'价钱',max_digits=5,decimal_places=2)
    isDelete=models.BooleanField(default=False)
    gunit=models.CharField(u'单位',max_length=20,default='500g')
    gclick=models.IntegerField(u'点击')
    gjianjie=models.CharField(max_length=200)
    gkucun=models.IntegerField(u'库存')
    gcontent=HTMLField(u'描述')
    # 引用外键
    gtype=models.ForeignKey(TypeInfo)
    # 商品对象名字返回
    def __str__(self):
        return self.gtitle.encode('utf-8')
    class Meta:
        verbose_name_plural='水果'
