#coding=utf-8

from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from df_user import user_decorator
from models import *

# 装饰器检测帐号是否登录
@user_decorator.login
def cart(request):
    # 查询用户登录信息
    uid=request.session['user_id']
    # 查询此用户的购物车
    carts=CartInfo.objects.filter(user_id=uid)
    # 构造上下文
    context={'title':'购物车',
             'page_name':1,
             'carts':carts,
    }
    # 渲染模板
    return  render(request,'df_cart/cart.html',context)

# 装饰器检测帐号是否登录
@user_decorator.login
def add(request,gid,count):
    #用户uid购买了gid商品，数量为count
    uid=request.session['user_id']
    gid=int(gid)
    count=int(count)
    #查询购物车中是否已经有此商品，如果有则数量增加，如果没有则更新
    carts=CartInfo.objects.filter(user_id=uid,goods_id=gid)
    # 如果购物车表中已经有了这条信息，那就增加购物车这条信息的购买数量
    if len(carts)>=1:
        cart=carts[0]
        cart.count=cart.count+count
    else:
        # 如果购物车表中没有这条商品信息，则新建一条记录，添加到表中
        # 构造购物车对象，赋予属性
        cart=CartInfo()
        cart.user_id=uid
        cart.goods_id=gid
        cart.count=count
    # 保存进数据库
    cart.save()
    # 如果是ajax请求则返回Json，否则转向购物车
    if request.is_ajax():
        count=CartInfo.objects.filter(user_id=request.session['user_id'])
        return JsonResponse({'count':count})
    else:
        return redirect('/cart/')




# 装饰器检测用户是否登录
@user_decorator.login
def edit(request,cart_id,count):
    # 购物车修改商品信息的异步函数
    try:
        # 查询数据库信息，修改后后进行保存
        cart=CartInfo.objects.get(pk=int(cart_id))
        count1=cart.count=int(count)
        cart.save()
        data={'ok':0}
    except Exception as e:
        data={'ok':count1}
    return JsonResponse(data)

@user_decorator.login
def delete(request,cart_id):
    # 删除购物车信息函数
    try:
        cart=CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data={'ok':1}
    except Exception as e:
        data={'ok':0}
    return JsonResponse(data)
