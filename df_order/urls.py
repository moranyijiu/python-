# coding=utf-8

from django.conf.urls import url
import views
# 订单应用路由分发
urlpatterns=[
    # 显示用户中心的订单表
    url(r'^$',views.order),
    # 订单提交处理视图
    url(r'^order_handle/',views.order_handle),
    # 直接购买
    url(r'^order(\d+)',views.order1),
    # 直接购买提交订单处理
    url(r'^order_handle1/',views.order_handle1),
    # 模拟支付视图
    url(r'^pay(\d+)/$',views.pay),
    # 统计销售信息
    url(r'^a/$',views.chart),
]