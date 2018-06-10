# coding=utf-8

from django.conf.urls import url
import views

# 购物车路由分发
urlpatterns=[
    # 购物车展示
    url(r'^$',views.cart),
    # 购物车商品增加
    url(r'^add(\d+)_(\d+)/$',views.add),
    # 购物车信息修改  异步
    url(r'^edit(\d+)_(\d+)/$',views.edit),
    # 购物车信息删除
    url(r'^delete(\d+)/$',views.delete),
]