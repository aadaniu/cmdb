# -*- coding: utf-8 -*-
# 2017-12-13
# by why

import time
import json
from django.shortcuts import render,render_to_response,HttpResponseRedirect,redirect
from django.http import HttpResponse

from opmanage.views.index import check_login, check_user_auth
from opmanage.forms.user import AddUserForm, DelUserForm,UpdataUserForm,GetUserForm
from opmanage.models import User_info
from lib.load_config import global_all_email_suffix
from lib.zabbix import zabbix


# 用于判定页面访问权限的下标
check_num = 1

@check_login
@check_user_auth(check_num=check_num)
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
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            email = username + '@' + global_all_email_suffix
            auth_num = 0
            auth_list = request.POST.getlist('auth')
            for i in auth_list:
                auth_num += int(i)
            auth_str = str(auth_num).rjust(20,'0')
            jumper = request.POST.get('jumper', None)
            vpn = request.POST.get('vpn', None)
            phone = request.POST.get('phone', None)
            department_id = request.POST.get('department', None)
            zabbix = request.POST.get('zabbix', None)
            git = request.POST.get('git', None)
            jenkins = request.POST.get('git', None)

            # 插入数据
            User_info.objects.create(username=username,password=password,email=email,auth=auth_str,jumper=jumper,
                                     vpn=vpn,phone=phone,department_id=department_id,zabbix=zabbix,git=git,jenkins=jenkins)

            # 创建VPN
            if vpn  == 't':
                try:
                    create_vpn(username,password,email)
                except:
                    pass
            # 创建跳板机
            if jumper == 't':
                try:
                    create_jumper(username,password,email)
                except:
                    pass
            # 创建zabbix用户
            if zabbix  == 't':
                # 如果创建失败
                if create_zabbix(username,password,phone)['status'] == False:
                    print 'zabbix no'
            # 创建git用户
            if git  == 't':
                try:
                    create_git(username,password,email)
                except:
                    pass
            # 创建jenkins用户
            if jenkins  == 't':
                try:
                    create_jenkins(username,password,email)
                except:
                    pass
            # 创建用户成功
            return HttpResponse('ok')

        # 字段验证不通过
        else:
            print add_userform.errors['username'][0]
            return render(request, "user/adduser.html", {'add_userform': add_userform})

    # 非POST请求
    else:
        add_userform = AddUserForm()
        return render(request,"user/adduser.html", {'add_userform': add_userform})


@check_login
@check_user_auth(check_num=check_num)
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
            if check_manage_password(request.session.get('username',None),manager_password) == False:
                # 添加权限报错，计划改到form
                return render(request, "/user/deluser.html", {'del_userform': del_userform})
            # 验证管理员用户通过
            else:
                # 删除权限用户
                # 删除用户
                User_info.objects.filter(username=username).delete()
                # 删除用户其他权限账户
                delete_zabbix(username)
                return HttpResponse('del %s' % username)
        # 字段验证不通过
        else:
            return render(request, "user/deluser.html", {'del_userform': del_userform})
    # 非POST请求
    else:
        del_userform = DelUserForm()
        return render(request, "user/deluser.html", {'del_userform': del_userform})


@check_login
@check_user_auth(check_num=check_num)
def get_user(request):
    """
        查询用户信息
    :param request:
    :return:
    """
    if request.method == "POST":
        get_userform = GetUserForm(request.POST)
        if get_userform.is_valid():
            username = request.POST.get('username')
            userinfo = User_info.objects.filter(username=username)
            return render(request, "user/getuserinfo.html", {'userinfo': userinfo})
    else:
        get_userform = GetUserForm()
        return render(request, "user/getuser.html", {'get_userform': get_userform})


@check_login
@check_user_auth(check_num=check_num)
def updata_user(request):
    """
        修改用户
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        updata_userform = UpdataUserForm(request.POST)
        # 字段验证通过
        if updata_userform.is_valid():
            manager_password = request.POST.get('manager_password', None)
            # 验证管理员权限不通过
            if check_manage_password(request.session.get('username', None), manager_password) == False:
                # 添加权限报错，计划改到form
                return render(request, "user/updatauser.html", {'updata_userform': updata_userform, 'error': updata_userform.errors})
            # 验证管理员用户通过
            else:
                username = request.POST.get('username')
                password = request.POST.get('password')
                phone = request.POST.get('phone')
                auth_num = 0
                auth_list = request.POST.getlist('auth')
                for i in auth_list:
                    auth_num += int(i)
                auth_str = str(auth_num).rjust(20,'0')
                jumper = request.POST.get('jumper')
                vpn = request.POST.get('vpn')
                department = request.POST.get('department')
                zabbix = request.POST.get('zabbix')
                git = request.POST.get('git')
                jenkins = request.POST.get('jenkins')
                if password != '':
                    updata_user_password(request,username,password)
                if auth_str != '':
                    updata_user_auth(request,username,auth_str)
                if jumper != '':
                    updata_user_jumper(request,username,jumper)
                if vpn != '':
                    updata_user_vpn(request,username,vpn)
                if phone != '':
                    updata_user_phone(request,username,phone)
                if department != '':
                    updata_user_department(request,username,department)
                if zabbix != '':
                    updata_user_zabbix(request,username,zabbix)
                if git !=  '':
                    updata_user_git(request,username,git)
                if jenkins !=  '':
                    updata_user_jenkins(request,username,jenkins)
                return HttpResponse('updata %s' % username)
        # 字段验证不通过
        else:
            print updata_userform.errors
            return render(request, "user/updatauser.html", {'updata_userform': updata_userform})
    # 非POST请求
    else:
        updata_userform = UpdataUserForm()
        return render(request, "user/updatauser.html", {'updata_userform': updata_userform})


def updata_user_password(request,username=None,password=None):
    """
        用于用户修改密码
    :param request:
    :return:
    """
    if request.method == 'POST':
        User_info.objects.filter(username=username).update(password=password)
    else:
        pass


def updata_user_auth(request,username=None,auth=None):
    """
        用于用户修改cmdb权限
    :param request:
    :return:
    """
    if request.method == 'POST':
        User_info.objects.filter(username=username).update(auth=auth)
    else:
        pass


def updata_user_vpn(request,username=None,vpn=None):
    """
        用于用户修改vpn权限
    :param request:
    :return:
    """
    if request.method == 'POST':
        User_info.objects.filter(username=username).update(vpn=vpn)
    else:
        pass


def updata_user_jumper(request,username=None,jumper=None):
    """
        用于用户修改jumper权限
    :param request:
    :return:
    """
    if request.method == 'POST':
        User_info.objects.filter(username=username).update(jumper=jumper)
    else:
        pass

def updata_user_phone(request,username=None,phone=None):
    """
        用于用户修改电话
    :param request:
    :return:
    """
    if request.method == 'POST':
        User_info.objects.filter(username=username).update(phone=phone)
    else:
        pass


def updata_user_department(request,username=None,department=None):
    """
        用于用户修改部门
    :param request:
    :return:
    """
    if request.method == 'POST':
        User_info.objects.filter(username=username).update(department=department)
    else:
        pass

def updata_user_zabbix(request,username=None,zabbix=None):
    """
        用于用户修改部门
    :param request:
    :return:
    """
    if request.method == 'POST':
        userinfo = User_info.objects.filter(username=username)
        userinfo.update(zabbix=zabbix)
        if zabbix == '1':
            create_zabbix(username, userinfo[0].password,userinfo[0].phone)
        else:
            delete_zabbix(username)
    else:
        pass

def updata_user_git(request,username=None,git=None):
    """
        用于用户修改部门
    :param request:
    :return:
    """
    if request.method == 'POST':
        User_info.objects.filter(username=username).update(git=git)
    else:
        pass

def updata_user_jenkins(request,username=None,jenkins=None):
    """
        用于用户修改部门
    :param request:
    :return:
    """
    if request.method == 'POST':
        User_info.objects.filter(username=username).update(jenkins=jenkins)
    else:
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


def create_git(username,password,email):
    """
        创建git用户
    :param username:
    :param password:
    :param email:
    :return:
    """
    pass


def create_jenkins(username,password):
    """
        创建jenkins用户
    :param username:
    :param password:
    :return:
    """
    pass


def create_zabbix(username,password,phone):
    """
        创建zabbix用户
    :param username:
    :param password:
    :param phone:
    :return:
    """
    z = zabbix()
    params = {'alias': username,
              'passwd': password}
    params['usrgrps'] = [{'usrgrpid': '7'}]
    params['user_medias'] = [
                                  {'mediatypeid': '1',
                                   'sendto': phone,
                                   'active': '0',
                                   'severity': '63',
                                   'period': '1-7,00:00-24:00'
                                  }
                            ]
    result = z.getdataZabbix('user.create', params)
    return result


def delete_zabbix(username):
    """
        删除zabbix用户
    :param username:
    :return:
    """
    z = zabbix()
    params = [z.username_to_id(username)]
    result = z.getdataZabbix('user.delete', params)
    return result


def check_manage_password(*args):
    """
        暂时用于删除业务逻辑
    :param args:
    :return:
    """
    pass


def get_message(request):
    """
        获取员工用户，部门和电话
    :param request:
    :return:
    """
    user_info = User_info.objects.all()
    return render(request, "user/getmessage.html", {'user_info': user_info})




def interface_user_phone(request):
    """
        ajax接口，用于返回用户，部门和电话
    :param request:
    :return:
    """

    result = {'status': False,
              'data': []}

    if request.POST.get('searchstr'):
        pass
    try:
        user_info = User_info.objects.all()
        for i in user_info:
            result['data'].append({'username':i['username'],'phone':i['phone'],'department':i['department'],})
        result['status'] = True
    except:
        pass
    return HttpResponse(json.dumps(result))
