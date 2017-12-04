# -*- coding: utf-8 -*-
# 2017-11-29
# by why

from django.shortcuts import render,render_to_response,HttpResponseRedirect,redirect
from django.http import HttpResponse

from opmanage.forms import UserForm, AddUserForm, DelUserForm
from opmanage.models import User_info
from lib.load_config import global_all_email_suffix

import time

def login(request):
    """
        用于用户登录
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        userform = UserForm(request.POST)
        # 字段验证通过
        if userform.is_valid():
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            # 登录验证成功
            # 计划挪到form
            if check_login(username,password):
                request.session['username'] = username
                request.session['auth'] = get_auth(username)
                return redirect('/login/')
            # 登录验证失败
            else:
                return render(request, "login.html", {'userform': userform, 'error': userform.errors})
        # 字段验证不通过
        else:
            return render(request, "login.html", {'userform': userform, 'error': userform.errors})
    # 非POST请求
    else:
        # 验证权限
        # 计划弄成装饰器
        if request.session.get('auth',None) == 1:
            return render(request, 'index.html')
        # 验证失败
        else:
            userform = UserForm()
            return render(request,"login.html", {'userform': userform})


def add_user(request):
    """
        添加用户
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        add_userform = AddUserForm(request.POST)
        # 字段验证通过
        if add_userform.is_valid():
            print global_all_email_suffix
            email = request.POST.get('email', None)
            username = email.replace('@' + global_all_email_suffix,'')
            password = request.POST.get('password', None)
            auth = request.POST.get('auth', None)
            jumper = request.POST.get('jumper', None)
            vpn = request.POST.get('vpn', None)
            phone = request.POST.get('phone', None)
            department = request.POST.get('department', None)
            zabbix = request.POST.get('zabbix', None)
            kibana = request.POST.get('kibana', None)

            # 插入数据
            User_info.objects.create(username=username,password=password,email=email,auth=auth,jumper=jumper,
                                     vpn=vpn,phone=phone,department=department,zabbix=zabbix,kibana=kibana)

            # 创建VPN
            if vpn:
                try:
                    create_vpn(username,password,email)
                except:
                    pass
            # 创建跳板机
            if jumper:
                try:
                    create_jumper(username,password,email)
                except:
                    pass
            # 创建zabbix用户
            if zabbix:
                try:
                    create_zabbix(username,password,email)
                except:
                    pass
            # 创建kibana用户
            if kibana:
                try:
                    create_kibana(username,password,email)
                except:
                    pass
            # 创建用户成功
            return HttpResponse('ok')

        # 字段验证不通过
        else:
            return render(request, "adduser.html", {'add_userform': add_userform, 'error': add_userform.errors})

    # 非POST请求
    else:
        add_userform = AddUserForm()
        return render(request,"adduser.html", {'add_userform': add_userform})


def del_user(request):
    """
        删除用户
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        del_userform = DelUserForm(request.POST)
        # 字段验证通过
        if del_userform.is_valid():
            username = request.POST.get('username', None)
            manager_password = request.POST.get('manager_password', None)
            # 验证管理员权限不通过
            if check_login(request.session.get('username',None),manager_password) == False:
                # 添加权限报错，计划改到form
                return render(request, "deluser.html", {'del_userform': del_userform, 'error': del_userform.errors})
            # 验证管理员用户通过
            else:
                # 删除权限用户
                # 删除用户
                User_info.objects.filter(username=username).delete()
                return HttpResponse('del %s' % username)
        # 字段验证不通过
        else:
            return render(request, "deluser.html", {'del_userform': del_userform, 'error': del_userform.errors})
    # 非POST请求
    else:
        del_userform = DelUserForm()
        return render(request, "deluser.html", {'del_userform': del_userform})


def logout(request):
    """
        用于用户退出
    :param request:
    :return:
    """
    request.session.set_expiry(0.1)
    time.sleep(0.2)
    return redirect('/login/')


def index(request):
    """
        浏览主页
    :param request:
    :return:
    """
    if request.session.get('auth') == 1:
        return render(request, 'index.html')
    else:
        return redirect('/login/')


def change_password(request):
    """
        用于用户修改密码
    :param request:
    :return:
    """
    pass


def change_user_info(request):
    """
        用于修改权限
    :param request:
    :return:
    """


def check_login_auth(auth):
    """
        登录权限判断
    :param request:
    :return:
    """
    if auth == 1:
        return True
    else:
        return False


def check_manage_auth(auth):
    """
        管理权限判断
    :param request:
    :return:
    """
    if auth == 1:
        return True
    else:
        return False


def get_auth(username):
    """
        获取当前用户权限
    :param username:
    :return:
    """
    user_info = User_info.objects.filter(username=username)
    auth = user_info[0].auth
    return auth


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


def create_kibana(username,password,email):
    """
        创建kibana用户
    :param username:
    :param password:
    :param email:
    :return:
    """
    pass


def create_zabbix(username,password,email):
    """
        创建zabbix用户
    :param username:
    :param password:
    :param email:
    :return:
    """
    pass



def change_user_info(request):
    """
        修改用户
    :param request:
    :return:
    """
    pass


def check_manage_password(*args):
    """
        暂时用于删除业务逻辑
    :param args:
    :return:
    """
    pass




