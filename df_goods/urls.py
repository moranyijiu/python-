#coding=utf-8

from django.conf.urls import url
from . import views
from views import *
# 主页路由分发
urlpatterns= [
    # 展示主页
    url('^$', views.index),
    # 类型商品详情
    url('^list(\d+)_(\d+)_(\d+)/$', views.list),
    # 单个商品展示
    url('^(\d+)/$', views.detail),
    # 搜索匹配
    url('^search/', MySearchView()),
]