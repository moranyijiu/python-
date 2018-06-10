#coding=utf-8

from django.contrib import admin
from models import OrderInfo
from models import OrderDetailInfo
from models import sales
# class OrderInfoAdmin(admin.ModelAdmin):
#     list_display = ['oid', 'user', 'odate', 'oIsPay', 'ototal', 'oaddress']
#     # date_hierarchy = 'odate'
#
# class OrderDetailInfoAdmin(admin.ModelAdmin):
#     list_display = ['goods', 'order', 'price']
#     fk_fields=['order']
# admin.site.register(OrderInfo, OrderInfoAdmin)
# admin.site.register(OrderDetailInfo, OrderDetailInfoAdmin)


# 外联
class OrderDetailInfoFor(admin.TabularInline):
    model = OrderDetailInfo

# 订单展示
class OrderInfoAdmin(admin.ModelAdmin):
    inlines = [OrderDetailInfoFor]
    list_display = ['user','odate','oIsPay','ototal']
# 发货清单
class OrderDetailInfoAdmin(admin.ModelAdmin):

    list_display = ['goods', 'order', 'price','count']
# 销量统计
class salesAdmin(admin.ModelAdmin):

    list_display = ['goods','count','totalprice']
    ordering = ('-count','-totalprice')
    list_filter = ['goods']


admin.site.register(OrderInfo,OrderInfoAdmin)
admin.site.register(OrderDetailInfo,OrderDetailInfoAdmin)
admin.site.register(sales,salesAdmin)


