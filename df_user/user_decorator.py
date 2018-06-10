#coding=utf-8

from django.shortcuts import redirect
from django.http import HttpResponseRedirect


# 如果未登录则转到登录页面
def login(func):
    def login_fun(request, *args, **kwargs):
        # 检测是否登录，如果已将登陆，直接跳转
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        # 如果未登录，记录当前页面，跳转到登陆页面
        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url', request.get_full_path())
            return red
    return login_fun
# 记录之前页面，登陆后跳转到之前的页面，而不是只跳转到固定页面


