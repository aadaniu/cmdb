# -*- coding: utf-8 -*-
# 2017-12-13
# by why

import time
import json
from django.shortcuts import render,render_to_response,HttpResponseRedirect,redirect
from django.http import HttpResponse

from opmanage.views.index import check_login, check_user_auth, to_page
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
            email = request.POST.get('email', None)
            jumper = request.POST.get('jumper', None)
            vpn = request.POST.get('vpn', None)
            phone = request.POST.get('phone', None)
            zabbix = request.POST.get('zabbix', None)
            git = request.POST.get('git', None)
            jenkins = request.POST.get('git', None)

            # 插入数据
            add_userform.save()

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
            return render(request, "opmanage/user/adduser.html", {'add_userform': add_userform})
    # 非POST请求
    else:
        add_userform = AddUserForm()
        return render(request,"opmanage/user/adduser.html", {'add_userform': add_userform})


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
            # 删除用户
            User_info.objects.filter(username=username).delete()
            # 删除用户其他权限账户
            delete_zabbix(username)
            return HttpResponse('del %s' % username)
        # 字段验证不通过
        else:
            return render(request, "opmanage/user/deluser.html", {'del_userform': del_userform})
    # 非POST请求
    else:
        username = request.GET.get('username')
        if username != None:
            del_userform = DelUserForm({'username': username})
        else:
            del_userform = DelUserForm()
        return render(request, "opmanage/user/deluser.html", {'del_userform': del_userform})


@check_login
@check_user_auth(check_num=check_num)
def get_user(request):
    """
        查询用户信息
    :param request:
    :return:
    """
        # POST请求
    if request.method == "POST":
        get_userform = GetUserForm(request.POST)
        # 字段验证通过
        if get_userform.is_valid():
            username = request.POST.get('username', None)
            every_page_sum = request.POST.get('every_page_sum', 20)
            pages = request.POST.get('pages', 1)
            if username == '' or username == None:
                user_list = User_info.objects.all()
            else:
                user_list = []
                for i in User_info.objects.all():
                    if username in i.username:
                        user_list.append(i)
            page_user_list = to_page(user_list, pages, every_page_sum)
            # 获取相关user信息
            return render(request, "opmanage/user/getuser.html", {'get_userform': get_userform, 'page_user_list': page_user_list})
        # 字段验证不通过
        else:
            return render(request, "opmanage/user/getuser.html", {'get_userform': get_userform})
    # 非POST请求
    else:
        every_page_sum = 20
        # 获取当前页码
        pages = request.GET.get('page') or 1
        # 创建回传前端表单，如果username存在，返回相user_name表单，否则返回空白表单
        username = request.GET.get('username', None)
        if username == '' or username == None:
            user_list = User_info.objects.all()
            get_userform = GetUserForm()
        else:
            user_list = []
            for i in User_info.objects.all():
                if username in i.username:
                    user_list.append(i)
            get_userform = GetUserForm({'username': username})
        page_user_list = to_page(user_list, pages, every_page_sum)
        return render(request, "opmanage/user/getuser.html", {'get_userform': get_userform, 'page_user_list': page_user_list})



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
            username = request.POST.get('username')
            password = request.POST.get('password')
            phone = request.POST.get('phone')
            auth = request.POST.get('auth')
            jumper = request.POST.get('jumper')
            vpn = request.POST.get('vpn')
            department = request.POST.get('department')
            zabbix = request.POST.get('zabbix')
            git = request.POST.get('git')
            jenkins = request.POST.get('jenkins')


            user = User_info.objects.get(username=username)
            updata_hostform = UpdataUserForm(request.POST, instance=user)
            updata_hostform.save()
            # if password != '':
            #     updata_user_password(request,username,password)
            # if auth_str != '':
            #     updata_user_auth(request,username,auth_str)
            # if jumper != '':
            #     updata_user_jumper(request,username,jumper)
            # if vpn != '':
            #     updata_user_vpn(request,username,vpn)
            # if phone != '':
            #     updata_user_phone(request,username,phone)
            # if department != '':
            #     updata_user_department(request,username,department)
            # if zabbix != '':
            #     updata_user_zabbix(request,username,zabbix)
            # if git !=  '':
            #     updata_user_git(request,username,git)
            # if jenkins !=  '':
            #     updata_user_jenkins(request,username,jenkins)
            return HttpResponse('updata %s' % username)
        # 字段验证不通过
        else:
            return render(request, "opmanage/user/updatauser.html", {'updata_userform': updata_userform})
    # 非POST请求
    else:
        username = request.GET.get('username')
        if username != None:
            user = User_info.objects.get(username=username)
            # 参考https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#modelform
            updata_userform = UpdataUserForm(instance=user)
        else:
            updata_userform = UpdataUserForm()
        return render(request, "opmanage/user/updatauser.html", {'updata_userform': updata_userform})



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
    return render(request, "opmanage/user/getmessage.html", {'user_info': user_info})




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
