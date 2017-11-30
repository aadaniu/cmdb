# -*- coding: utf-8 -*-
# 2017-11-29
# by why

from django.shortcuts import render,render_to_response,HttpResponseRedirect
from cmdb_main.forms import UserForm

def login(request):
    """
        用于用户登录
    :param request:
    :return:
    """
    if request.method == "POST":
        userform = UserForm(request.POST)
        request.POST.get('username', None)
        request.POST.get('password', None)

        # 验证码
        return render(request,"login.html",{'userform': userform, 'error': userform.errors})

    else:
        userform = UserForm()
        return render(request,"login.html", {'userform': userform})


def logout(request):
    """
        用于用户退出
    :param request:
    :return:
    """
    pass


def index(request):
    """
        浏览主页
    :param request:
    :return:
    """
    pass


def auth(request):
    """
        权限判断，理论是一个装饰器
    :param request:
    :return:
    """
    pass

def is_login(request):
    """
        登录判断，
    :param request:
    :return:
    """

