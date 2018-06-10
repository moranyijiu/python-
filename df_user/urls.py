#coding=utf-8

from django.conf.urls import url
import views
#用户应用内的路由分发
urlpatterns=[
    #用户注册
    url(r'^register/$',views.register),
    #用户注册处理
    url(r'^register_handle/$',views.register_handle),
    #用户登陆
    url(r'^login/$',views.login),
    #用户登陆出来
    url(r'^login_handle/$',views.login_handle),
    #用户中心显示
    url(r'^info/$',views.info),
    #用户信息补全
    url(r'^site/$',views.site),
    #用户退出登陆
    url(r'^logout/$',views.logout),
    #用户查看自己的订单
    url(r'^order(\d*)/$',views.order),
    # 修改密码页面展示
    url(r'^passwd/',views.passwd),
    # 修改密码处理逻辑
    url(r'passwd_handle',views.passwd_handle),
]