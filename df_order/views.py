#coding=utf-8

from django.http import HttpResponse
from django.shortcuts import render,redirect
from df_user import user_decorator
from df_user.models import UserInfo
from df_cart.models import CartInfo
from df_goods.models import GoodsInfo
from django.db import transaction
from models import *
from datetime import datetime
from decimal import Decimal
import qrcode
from django.utils.six import BytesIO
import re
# 购物车生成订单逻辑，非直接购买生成订单
# 装饰器判断是否有用户登录
@user_decorator.login
def order(request):
    #查询用户对象
    user = UserInfo.objects.get(id=request.session['user_id'])
    #根据提交查询购物车信息
    get=request.GET
    cart_ids=get.getlist('cart_id')
    print cart_ids
    cart_ids1=[int(item) for item in cart_ids]
    carts=CartInfo.objects.filter(goods_id__in=cart_ids1).filter(user_id=user.id)
    # 构造上下文
    context={
             'title':'提交订单',
             'user':user,
             'page_name':1,
             'carts':carts,
             'cart_ids':','.join(cart_ids),
             }
    return render(request,'df_order/order.html',context)


# 购物车购买订单处理逻辑过程，非直接购买逻辑处理
'''
事务：一旦操作失败则全部回退
1 创建订单对象
2 创建商品的库存
3 创建详单对象
4 修改商品库存
5 删除购物车
'''
# 数据库事物装饰器，需要导入包
@transaction.atomic()
# 装饰器判断是都有用户登录
@user_decorator.login
def order_handle(request):
    #存一个回退点，如果事物失败，回退到这里
    tran_id=transaction.savepoint()
    #接受购物车编号
    cart_ids=request.POST.get('cart_ids')
    try:
        #创建订单对象
        order=OrderInfo()
        # 获取目前时间
        now=datetime.now()
        uid=request.session['user_id']
        # 订单号根据时间生成
        order.oid='%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id=uid
        order.odate=now
        order.ototal=Decimal(request.POST.get('total'))
        order.oaddress = request.POST.get('address')
        # 订单对象保存到数据苦库中
        order.save()
        #创建详单对象
        cart_ids1=[int(item) for item in cart_ids.split(',')]
        print cart_ids1
        # 订单中每个商品拿出来进行处理
        for id1 in cart_ids1:
            # 创建订单详表对象
            detail=OrderDetailInfo()
            detail.order=order
            #查询购物车信息
            cart=CartInfo.objects.filter(goods_id=id1).filter(user_id=uid)
            #判断商品库存
            good=cart[0].goods
            goods=GoodsInfo.objects.get(gtitle=good)
            if goods.gkucun>=cart[0].count:#如果哭u才能大于购买量
                #减少商品库存gkucun
                goods.gkucun-=cart[0].count
                goods.save()
                #完善详单信息
                detail.goods_id=goods.id
                detail.price=goods.gprice
                detail.count=cart[0].count
                detail.save()
                #删除购物车数据
                cart.delete()
            else:#如果库存小于购买数量
                #事物回滚到订的回退点
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
                #return HttpResponse('no')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print '==========%s======='%e
        transaction.savepoint_rollback(tran_id)

        # return HttpResponse('ok')
    return redirect('/user/order/')

# 装饰器判断是否有用户登录
@user_decorator.login
def pay(request,oid):
    # 查询到这个订单信息
    order=OrderInfo.objects.get(oid=oid)
    # 修改支付信息
    order.oIsPay=True
    # 将对象保存到数据库中
    order.save()
    # 根据收到的订单号构造二维码
    img = qrcode.make('订单号\n         '+oid+'\n       '+'谢谢你来到天天水果购物，祝你生活愉快！')

    buf = BytesIO()
    img.save(buf)
    image_stream = buf.getvalue()
    # 构造上下文
    context={
                'order':order,
                'img':image_stream,
             }
    #，付帐后，统计销量
    # 查询发货单，统计销量信息
    all = OrderDetailInfo.objects.all().filter(isTrue=False)
    # 遍历
    for a in all:
        # 查询销量表中是否已有此数据，如果则是增加信息，若没有则添加进去
        sale_number = sales.objects.filter(goods=a.goods)
        # 数据库中有此信息
        if len(sale_number) == 1:
            # 销量加上去
            sale1 = sale_number[0]
            sale1.count += a.count
            # 算出此部分销售额
            price1 = a.price * a.count
            sale1.totalprice += price1
            sale1.save()
            a.isTrue=True
            a.save()
        # 数据库中没有此信息
        else:
            sale = sales()
            sale.goods = a.goods
            sale.count = a.count
            # 计算销售额
            price2 = a.count * a.price
            sale.totalprice = price2
            sale.save()
            a.isTrue=True
            a.save()
    # return render(request,'df_order/pay.html',context)
    response = HttpResponse(image_stream, content_type="image/png")
    return response

# 立即购买直接跳转到订单页面处理
# 装饰器判断是否有用户登录
@user_decorator.login
def order1(request,good_count):
    #查询用户对象
    user = UserInfo.objects.get(id=request.session['user_id'])
    # 接受立即购买的数量
    count=good_count
    #根据提交查询商品信息
    get=request.GET
    goods_ids=get.get('good_id')
    # 查询到这个商品
    goods=GoodsInfo.objects.get(id=goods_ids)
    # 构造上下文
    context={
             'title':'提交订单',
             'user':user,
             'page_name':1,
             'goods':goods,
             'count':count,
             }
    return render(request,'df_order/order1.html',context)

# 立即购买订单处理逻辑
# 数据库事物装饰器，需要导入包
@transaction.atomic()
# 装饰器判断是都有用户登录
@user_decorator.login
def order_handle1(request):
    #存一个回退点，如果事物失败，回退到这里
    tran_id=transaction.savepoint()
    # 接受商品id
    good_id=request.POST.get('good_id')
    # 获取商品数量
    count=request.POST.get('count')
    # 查询到这个商品
    good = GoodsInfo.objects.get(id=good_id)
    # 得到此商品价钱
    goodprice=good.gprice
    try:
        #创建订单对象
        order=OrderInfo()
        # 获取目前时间
        now = datetime.now()
        uid = request.session['user_id']
        # 订单号根据时间生成
        order.oid='%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        # 订单生成者
        order.user_id=uid
        # 订单生成时间
        order.odate=now
        # 总价等于商品的价钱*数量
        price=float(goodprice)
        count1=float(count)
        zongjia=price*count1
        order.ototal=zongjia+10
        # 订单收货地址
        order.oaddress = request.POST.get('address')
        # 订单对象保存到数据苦库中
        order.save()
        #创建详单对象
        good_id1=int(good_id)
        # 数量处理
        detail=OrderDetailInfo()
        detail.order=order
        shangpin=GoodsInfo.objects.get(id=good_id)
        if shangpin.gkucun>count1:
            shangpin.gkucun-=count1
            shangpin.save()
            detail.goods_id=good_id1
            detail.price=shangpin.gprice
            detail.count=count1
            detail.save()
        else:  # 如果库存小于购买数量
            # 事物回滚到订的回退点
            transaction.savepoint_rollback(tran_id)
            return HttpResponse('重新购买，出错了！！！')
        # 一切正常，事物提交
        transaction.savepoint_commit(tran_id)
    # 抛出异常，打印异常
    except Exception as e:
        print '==========%s=======' % e
        transaction.savepoint_rollback(tran_id)
    # 重定向到用户中心查看订单
    return redirect('/user/order/')

# 统计图表视图
def chart(request):
    # 查询所有销售的信息
    saleall=sales.objects.all()

    #柱状图所需数据
    # 将销售的商品名称构建成列表
    list_name=[]
    # 销量构建成列表
    list_count=[]
    # 销售额构建成列表
    list_qian=[]
    for s in saleall:
        a=s.goods.gtitle
        # 构建列表
        list_name.append(str(a))
        list_count.append(int(s.count))
        list_qian.append(float(s.totalprice))

    #圆饼图所需数据
    saleall1=sales.objects.all()
    list=[]
    for s2 in saleall1:
        list.append(s2)

    #折线图销售额前5所需数据
    saleall2=sales.objects.all().order_by('-totalprice')[0:5]
    list1_name=[]
    list1_count=[]
    list1_qian=[]
    for s2 in saleall2:
        a = s2.goods.gtitle
        # 构建列表
        list1_name.append(str(a))
        list1_count.append(int(s2.count))
        list1_qian.append(float(s2.totalprice))
    #折线统计图销量前5所需数据
    saleall3 = sales.objects.all().order_by('-count')[0:5]
    list2_name = []
    list2_count = []
    list2_qian = []
    for s2 in saleall3:
        a = s2.goods.gtitle
        # 构建列表
        list2_name.append(str(a))
        list2_count.append(int(s2.count))
        list2_qian.append(float(s2.totalprice))
    context={
        'list_name':list_name,
        'list_count':list_count,
        'list_qian':list_qian,
        'list1_name':list1_name,
        'list1_count':list1_count,
        'list1_qian':list1_qian,
        'list2_name': list2_name,
        'list2_count': list2_count,
        'list2_qian': list2_qian,
        'list':list,
    }
    return render(request,'df_order/chart.html',context)
