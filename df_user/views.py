# coding=utf-8

from django.shortcuts import render, redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse
from . import user_decorator
from df_goods.models import *
from django.core.paginator import Paginator, Page
from df_order.models import *


# 展示注册界面
def register(request):
    return render(request, 'df_user/register.html')


# 用户注册处理逻辑
def register_handle(request):
    # 接受用户输入，POST方式
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码是否一致,
    if upwd != upwd2:
        return redirect('/user/register/')
    # 密码加密，采用sha1加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    # 将用户信息保存进数据库
    user.save()
    # 注册成功,转到登陆页面
    return redirect('/user/login/')

#修该密码页面展示
def passwd(request):
    return render(request,'df_user/passwd.html')

#修改密码处理逻辑
def passwd_handle(request):
    # 接受用户输入，POST方式
    post = request.POST
    uname=post.get('user_name')
    uemail=post.get('email')
    pwd1=post.get('pwd1')
    pwd2=post.get('pwd2')
    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)  # []
    if len(users)==1:
        #判断邮箱信息
        if users[0].uemail==uemail:
            if pwd1==pwd2:
                # 密码加密，采用sha1加密
                s1 = sha1()
                s1.update(pwd1)
                pwd3 = s1.hexdigest()
                user=users[0]
                user.upwd=pwd3
                user.save()
                # 修改密码成功,转到登陆页面
                return redirect('/user/login/')
            else:
                return HttpResponse('两次输入密码不一样')
        else:
            return HttpResponse('邮箱输入错误！')
    else:
        return HttpResponse('查无此人，请返回后重新输入！')


# 异步处理用户名重复
def register_exist(request):
    # 采用get请求
    uname = request.GET.get('uname')
    # 查询数据库中采用这个用户名的数量，如果为0，那就是未被使用，可以使用
    count = UserInfo.objects.filter(uname=uname).count()
    # 展示模板
    return JsonResponse({'count': count})


# 登陆处理
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登陆', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)

# 登陆处理
def login_handle(request):
    # 接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)  # []
    # 判断：如果未查询到则用户名错，如果查到则判断密码是否正确，正确则转到
    if len(users) == 1:
        # 将传来的密码sha1加密后与数据库加密过的密码对比
        s1 = sha1()
        s1.update(upwd)
        # 判断密码是否正确
        if s1.hexdigest() == users[0].upwd:

            url = request.COOKIES.get('url', '/goods/')
            red = HttpResponseRedirect(url)
            # 记住用户名
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        # 密码错误转到用户登陆页
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    # 没有这个用户名，转到登陆页
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)

# 退出登陆
def logout(request):
    # 清除session信息
    request.session.flush()
    # 转向到首页
    return redirect('/goods/')

#装饰器检测是否帐号已经登陆
@user_decorator.login
def info(request):
    # 最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    # 如果没浏览则返回空的的浏览列表
    if goods_ids1==['']:
        goods_list==[]
    # 如果浏览了则返浏览的信息
    else:
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    # 根据登陆的信息，查询登陆用户的各项信息
    user = UserInfo.objects.get(id=request.session['user_id'])
    user_eamil = user.uemail
    user_address = user.uaddress
    user_phone = user.uphone
    # 构造上下文
    context = {'title': '用户中心',
               'user_eamil': user_eamil,
               'user_name': request.session['user_name'],
               'user_address': user_address,
               'user_phone': user_phone,
               # 最近浏览信息
               'goods_list': goods_list,
               }
    # 渲染模板
    return render(request, 'df_user/user_center_info.html', context)

# 装饰器检测帐号是否登陆
@user_decorator.login
def order(request, pindex):
    # 查询这个账户的订单信息，倒序排列
    order_list = OrderInfo.objects.filter(user_id=request.session['user_id']).order_by('-oid')
    # 分页展示，每页最多展示2个订单
    paginator = Paginator(order_list, 2)
    # 传来url中的页面信息如果为空，就展示第一页
    if pindex == '':
        pindex = '1'
    page = paginator.page(int(pindex))
    # 构造上下文传递
    context = {'title': '天天生鲜用户中心',
               # 分页信息
               'paginator': paginator,
               'page': page, }
    # 渲染模板
    return render(request, 'df_user/user_center_order.html', context)

# 装饰检测帐号是否登陆
@user_decorator.login
def site(request):
    # 根据session的信息查询用户的相应信息
    user = UserInfo.objects.get(id=request.session['user_id'])
    # 如果为POST请求，则是修改信息，构造对象存储，保存
    if request.method == 'POST':
        post = request.POST
        user.ushow = post.get('ushow')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title': '用户中心', 'user': user}
    # 渲染模板
    return render(request, 'df_user/user_center_site.html', context)

