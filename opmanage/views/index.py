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
            if check_login(username,password):
                return HttpResponse('login')
            else:
                return HttpResponse('not login')
        else:
            return render(request, "login.html", {'userform': userform, 'error': userform.errors})
    else:
        userform = UserForm()
        return render(request,"login.html", {'userform': userform})


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
            email = request.POST.get('email', None)
            auth = request.POST.get('auth', None)
            jumper = request.POST.get('jumper', None)
            vpn = request.POST.get('vpn', None)
            phone = request.POST.get('phone', None)
            department = request.POST.get('department', None)
            ccj_admin = request.POST.get('ccj_admin', None)
            cct_admin = request.POST.get('ccj_admin', None)

            # 判断用户是否存在，不存在添加错误返回
            if not check_userexit(username):
                pass

            # 插入数据
            User_info.objects.create(username=username,password=password,email=email,auth=auth,jumper=jumper,
                                     vpn=vpn,phone=phone,department=department,ccj_admin=ccj_admin,cct_admin=cct_admin)

            if vpn:
                try:
                    create_vpn(username,password,email)
                except:
                    pass
            if jumper:
                try:
                    create_jumper(username,password,email)
                except:
                    pass
            if ccj_admin:
                try:
                    create_ccjadmin(username,password,email)
                except:
                    pass
            if cct_admin:
                try:
                    create_cctadmin(username,password,email)
                except:
                    pass
        else:
            return render(request, "adduser.html", {'add_userform': add_userform, 'error': add_userform.errors})
    else:
        userform = AddUserForm()
        return render(request,"adduser.html", {'userform': userform})


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


def check_auth(request):
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




def check_userexit(username):
    """
        检查用户名是否存在
    :param username:
    :return:
    """
    check_userexit_status = User_info.objects.filter(username=username).count()
    if check_userexit_status == 1:
        return True
    else:
        return False

def check_emailexit(email):
    """
        检查邮箱是否存在
    :param email:
    :return:
    """
    pass


def create_vpn(username,email):
    """
        创建vpn
    :param username:
    :param email:
    :return:
    """
    pass

def create_jumper(username,password,email):
    """
        创建跳板机账户
    :param username:
    :param password:
    :param email:
    :return:
    """
    pass


def create_ccjadmin(username,password,email):
    """
        创建楚楚街用户
    :param username:
    :param password:
    :param email:
    :return:
    """
    pass


def create_cctadmin(username,password,email):
    """
        创建楚楚通用户
    :param username:
    :param password:
    :param email:
    :return:
    """
    pass

def del_user(request):
    """
        删除用户
    :param request:
    :return:
    """
    pass

def change_user(request):
    """
        修改用户
    :param request:
    :return:
    """
    pass


def check_login(username,password):
    """
        验证用户名密码是否正确
    :param username: 用户名
    :param password: 密码
    :return:
    """
    check_login_status = User_info.objects.filter(username=username,password=password).count()
    if check_login_status == 1:
        return True
    else:
        return False