# -*- coding: utf-8 -*-
# 2017-11-29
# by why

from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.http import HttpResponse

from opmanage.forms import UserForm, AddUserForm
from opmanage.models import User_info

def login(request):
    """
        用于用户登录
    :param request:
    :return:
    """
    if request.method == "POST":
        userform = UserForm(request.POST)
        if userform.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            check_login = User_info.objects.filter(username=username,password=password).count()
            print check_login
            if check_login == 1:
                return HttpResponse('login')
            else:
                return HttpResponse('not login')
        else:
            return render(request, "login.html", {'userform': userform, 'error': userform.errors})
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

def add_user(request):
    """
        添加用户
    :param request:
    :return:
    """
    if request.method == "POST":
        add_userform = AddUserForm(request.POST)
        if add_userform.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            check_login = User_info.objects.filter(username=username,password=password).count()
            print check_login
            if check_login == 1:
                return HttpResponse('login')
            else:
                return HttpResponse('not login')
        else:
            return render(request, "login.html", {'userform': userform, 'error': userform.errors})
    else:
        userform = AddUserForm()
        return render(request,"login.html", {'userform': userform})


def del_user(request):
    """
        删除用户
    :param request:
    :return:
    """

def change_user(request):
    """
        删除用户
    :param request:
    :return:
    """

