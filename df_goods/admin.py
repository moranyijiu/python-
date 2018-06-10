# coding=utf-8

from django.contrib import admin
from models import TypeInfo
from models import GoodsInfo

# # 后台类型管理
# class TypeInfoAdmin(admin.ModelAdmin):
#     # 展示字段
#     list_display = ['id', 'ttitle']

# 后台商品管理
class GoodsInfoAdmin(admin.ModelAdmin):
    # 查询字段设定
    search_fields = ['gtitle']
    # 每页最多显示的信息
    list_per_page = 10
    # 展示的信息
    list_display = ['id', 'gtitle', 'gprice', 'gunit', 'gclick', 'gkucun', 'gcontent', 'gtype']
    list_filter = ['gtitle']

# 后台名字修改
admin.site.site_header = "天天水果商家管理"
admin.site.site_title = "天天水果后台"
# 注册两个信息进行管理
# admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)
