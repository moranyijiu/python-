# coding=utf-8

from django.contrib import admin
from models import UserInfo

# 利用装饰器添加到后台管理
@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    # 展示的信息
    list_display = ['uname', 'uemail', 'ushow', 'uaddress', 'uyoubian', 'uphone']
    # 可修改的信息内容
    fields = ['uname', 'uemail', 'ushow', 'uaddress', 'uyoubian', 'uphone']
    # 每页最大显示数目
    list_per_page = 10
    # 查询字段设定
    search_fields = ['uname']
