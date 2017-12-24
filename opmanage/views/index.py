# -*- coding: utf-8 -*-
# 2017-11-29
# by why

import time
from django.shortcuts import render,render_to_response,HttpResponseRedirect,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect


from opmanage.forms.index import LoginUserForm
from opmanage.models import User_info


def check_login(func):
    """
        装饰器，用于判定登录状态
    :param func:
    :return:
    """
    def check_login_status(request, *args, **kwargs):
        # print 'check_login装饰器'
        # 验证登录状态通过，正常显示
        if request.session.get('login_status', None) == 1:
            # print 'check_login验证登录状态通过，正常显示ok'
            r = func(request)
            return r
        # 验证登录状态不通过，跳转到登录页面
        else:
            # print 'check_login验证登录状态不通过，跳转到登录页面no'
            return redirect('/index/login/?nextpath=%s'% request.path)

    return check_login_status

def check_user_auth(check_num):
    """
        装饰器，用于检测用户页面访问权限
    :param func:
    :param check_num: 权限认证级别，1为user，2为host
    :return:
    """
    def check_user_auth_1(func):
        def check_user_auth_2(request):
            print 'check_user_auth'
            # 取负用作下标
            # 不懂为什么这里写check_num -= 0不行，必须传递给一个变量才能实现。
            local_check_num = int(check_num)
            local_check_num = 0 - local_check_num
            auth = request.session.get('auth')
            # 验证权限通过
            if str(auth)[local_check_num] == '1':
                print 'check_user_auth验证权限通过ok'
                return func(request)
            else:
                print 'check_user_auth验证权限不通过no'
                return HttpResponse('no')
        return check_user_auth_2
    return check_user_auth_1

@csrf_protect
def login(request):
    """
        用于用户登录
    :param request:
    :param nextpath:跳转路径
    :return:
    """
    # POST请求
    if request.method == "POST":
        userform = LoginUserForm(request.POST)
        # 字段验证通过
        if userform.is_valid():
            username = request.POST.get('username', None)
            nextpath = request.POST.get('nextpath', None)
            # 添加session
            request.session['username'] = username
            request.session['auth'] = get_auth(username)
            request.session['login_status'] = 1
            return redirect(nextpath)
        # 字段验证不通过
        else:
            return render(request, "index/login.html", {'userform': userform, 'error': userform.errors})
    # 非POST请求
    else:
        # 获取登录前要访问的url
        nextpath = request.GET.get('nextpath') or '/index/index/'
        userform = LoginUserForm({'nextpath': nextpath})
        return render(request, "index/login.html", {'userform': userform})


def index(request):
    """
        浏览主页
    :param request:
    :return:
    """
    return render(request, 'index/index.html')


def logout(request):
    """
        用于用户退出
    :param request:
    :return:
    """
    request.session.set_expiry(0.1)
    time.sleep(0.2)
    return redirect('/index/login/')


def get_auth(username):
    """
        获取当前用户权限
    :param username:
    :return:
    """
    user_info = User_info.objects.filter(username=username)
    auth = user_info[0].auth
    return auth


def page_4xx(request):
    """
        返回4xx错误页面
    """
    return render_to_response("4xx.html")



#
# @check_login
# @check_user_auth(check_num=check_num)
# def add_user(request):
#     """
#         添加用户
#     :param request:
#     :return:
#     """
#     # POST请求
#     if request.method == "POST":
#         add_userform = AddUserForm(request.POST)
#         # 字段验证通过
#         if add_userform.is_valid():
#             email = request.POST.get('email', None)
#             username = email.replace('@' + global_all_email_suffix,'')
#             password = request.POST.get('password', None)
#             auth = 0
#             auth_list = request.POST.getlist('cmdb_auth')
#             for i in auth_list:
#                 auth += int(i)
#             print auth
#             jumper = request.POST.get('jumper', None)
#             vpn = request.POST.get('vpn', None)
#             phone = request.POST.get('phone', None)
#             department = request.POST.get('department', None)
#             zabbix = request.POST.get('zabbix', None)
#             kibana = request.POST.get('kibana', None)
#
#             # 插入数据
#             User_info.objects.create(username=username,password=password,email=email,auth=auth,jumper=jumper,
#                                      vpn=vpn,phone=phone,department=department,zabbix=zabbix,kibana=kibana)
#
#             # 创建VPN
#             if vpn:
#                 try:
#                     create_vpn(username,password,email)
#                 except:
#                     pass
#             # 创建跳板机
#             if jumper:
#                 try:
#                     create_jumper(username,password,email)
#                 except:
#                     pass
#             # 创建zabbix用户
#             if zabbix:
#                 # 如果创建失败
#                 if create_zabbix(username,password,phone)['status'] == False:
#                     print 'zabbix no'
#             # 创建kibana用户
#             if kibana:
#                 try:
#                     create_kibana(username,password,email)
#                 except:
#                     pass
#             # 创建用户成功
#             return HttpResponse('ok')
#
#         # 字段验证不通过
#         else:
#             return render(request, "adduser.html", {'add_userform': add_userform, 'error': add_userform.errors})
#
#     # 非POST请求
#     else:
#         add_userform = AddUserForm()
#         return render(request,"adduser.html", {'add_userform': add_userform})
#
#
# def del_user(request):
#     """
#         删除用户
#     :param request:
#     :return:
#     """
#     # POST请求
#     if request.method == "POST":
#         del_userform = DelUserForm(request.POST)
#         # 字段验证通过
#         if del_userform.is_valid():
#             username = request.POST.get('username', None)
#             manager_password = request.POST.get('manager_password', None)
#             # 验证管理员权限不通过
#             if check_login(request.session.get('username',None),manager_password) == False:
#                 # 添加权限报错，计划改到form
#                 return render(request, "deluser.html", {'del_userform': del_userform, 'error': del_userform.errors})
#             # 验证管理员用户通过
#             else:
#                 # 删除权限用户
#                 # 删除用户
#                 User_info.objects.filter(username=username).delete()
#                 # 删除用户其他权限账户
#                 delete_zabbix(username)
#                 return HttpResponse('del %s' % username)
#         # 字段验证不通过
#         else:
#             return render(request, "deluser.html", {'del_userform': del_userform, 'error': del_userform.errors})
#     # 非POST请求
#     else:
#         del_userform = DelUserForm()
#         return render(request, "deluser.html", {'del_userform': del_userform})
#
#
# def get_user(request):
#     """
#         查询用户信息
#     :param request:
#     :return:
#     """
#     if request.method == "POST":
#         get_userform = GetUserForm(request.POST)
#         if get_userform.is_valid():
#             username = request.POST.get('username')
#             userinfo = User_info.objects.filter(username=username)
#             return render(request, "getuserinfo.html", {'userinfo': userinfo})
#     else:
#         get_userform = GetUserForm()
#         return render(request, "getuser.html", {'get_userform': get_userform})
#
#
# def updata_user(request):
#     """
#         修改用户
#     :param request:
#     :return:
#     """
#     # POST请求
#     if request.method == "POST":
#         updata_userform = UpdataUserForm(request.POST)
#         # 字段验证通过
#         if updata_userform.is_valid():
#             manager_password = request.POST.get('manager_password', None)
#             # 验证管理员权限不通过
#             if check_login(request.session.get('username', None), manager_password) == False:
#                 # 添加权限报错，计划改到form
#                 return render(request, "updatauser.html", {'updata_userform': updata_userform, 'error': updata_userform.errors})
#             # 验证管理员用户通过
#             else:
#                 username = request.POST.get('username')
#                 password = request.POST.get('password')
#                 auth = request.POST.get('auth')
#                 jumper = request.POST.get('jumper')
#                 vpn = request.POST.get('vpn')
#                 phone = request.POST.get('phone')
#                 department = request.POST.get('department')
#                 zabbix = request.POST.get('zabbix')
#                 kibana = request.POST.get('kibana')
#                 if password != '':
#                     updata_user_password(request,username,password)
#                 if auth != '':
#                     updata_user_auth(request,username,auth)
#                 if jumper != '':
#                     updata_user_jumper(request,username,jumper)
#                 if vpn != '':
#                     updata_user_vpn(request,username,vpn)
#                 if phone != '':
#                     updata_user_phone(request,username,phone)
#                 if department != '':
#                     updata_user_department(request,username,department)
#                 if zabbix != '':
#                     updata_user_zabbix(request,username,zabbix)
#                 if kibana !=  '':
#                     updata_user_kibana(request,username,kibana)
#                 return HttpResponse('updata %s' % username)
#         # 字段验证不通过
#         else:
#             return render(request, "updatauser.html", {'updata_userform': updata_userform, 'error': updata_userform.errors})
#     # 非POST请求
#     else:
#         updata_userform = UpdataUserForm()
#         return render(request, "updatauser.html", {'updata_userform': updata_userform})
#
#
# def updata_user_password(request,username=None,password=None):
#     """
#         用于用户修改密码
#     :param request:
#     :return:
#     """
#     if request.method == 'POST':
#         if check_manage_auth(request.session.get('auth',None)):
#             User_info.objects.filter(username=username).update(password=password)
#     else:
#         pass
#
#
# def updata_user_auth(request,username=None,auth=None):
#     """
#         用于用户修改cmdb权限
#     :param request:
#     :return:
#     """
#     if request.method == 'POST':
#         if check_manage_auth(request.session.get('auth',None)):
#             User_info.objects.filter(username=username).update(auth=auth)
#     else:
#         pass
#
#
# def updata_user_vpn(request,username=None,vpn=None):
#     """
#         用于用户修改vpn权限
#     :param request:
#     :return:
#     """
#     if request.method == 'POST':
#         if check_manage_auth(request.session.get('auth',None)):
#             User_info.objects.filter(username=username).update(vpn=vpn)
#     else:
#         pass
#
#
# def updata_user_jumper(request,username=None,jumper=None):
#     """
#         用于用户修改jumper权限
#     :param request:
#     :return:
#     """
#     if request.method == 'POST':
#         if check_manage_auth(request.session.get('auth',None)):
#             User_info.objects.filter(username=username).update(jumper=jumper)
#     else:
#         pass
#
# def updata_user_phone(request,username=None,phone=None):
#     """
#         用于用户修改电话
#     :param request:
#     :return:
#     """
#     if request.method == 'POST':
#         if check_manage_auth(request.session.get('auth',None)):
#             User_info.objects.filter(username=username).update(phone=phone)
#     else:
#         pass
#
#
# def updata_user_department(request,username=None,department=None):
#     """
#         用于用户修改部门
#     :param request:
#     :return:
#     """
#     if request.method == 'POST':
#         if check_manage_auth(request.session.get('auth',None)):
#             User_info.objects.filter(username=username).update(department=department)
#     else:
#         pass
#
# def updata_user_zabbix(request,username=None,zabbix=None):
#     """
#         用于用户修改部门
#     :param request:
#     :return:
#     """
#     if request.method == 'POST':
#         if check_manage_auth(request.session.get('auth',None)):
#             userinfo = User_info.objects.filter(username=username)
#             userinfo.update(zabbix=zabbix)
#             if zabbix == '1':
#                 create_zabbix(username, userinfo[0].password,userinfo[0].phone)
#             else:
#                 delete_zabbix(username)
#     else:
#         pass
#
# def updata_user_kibana(request,username=None,kibana=None):
#     """
#         用于用户修改部门
#     :param request:
#     :return:
#     """
#     if request.method == 'POST':
#         if check_manage_auth(request.session.get('auth',None)):
#             User_info.objects.filter(username=username).update(kibana=kibana)
#     else:
#         pass
#
# def check_login_auth(auth):
#     """
#         登录权限判断
#     :param request:
#     :return:
#     """
#     if auth == 1:
#         return True
#     else:
#         return False
#
#
# def check_manage_auth(auth):
#     """
#         管理权限判断
#     :param request:
#     :return:
#     """
#     if str[-1] == 1:
#         return True
#     else:
#         return False
#
#
# def get_auth(username):
#     """
#         获取当前用户权限
#     :param username:
#     :return:
#     """
#     user_info = User_info.objects.filter(username=username)
#     auth = user_info[0].auth
#     return auth
#
#
# def check_login(username,password):
#     """
#         验证用户名密码是否正确
#     :param username: 用户名
#     :param password: 密码
#     :return:
#     """
#     check_login_status = User_info.objects.filter(username=username,password=password).count()
#     if check_login_status == 1:
#         return True
#     else:
#         return False
#
# def create_vpn(username,email):
#     """
#         创建vpn
#     :param username:
#     :param email:
#     :return:
#     """
#     pass
#
# def create_jumper(username,password,email):
#     """
#         创建跳板机账户
#     :param username:
#     :param password:
#     :param email:
#     :return:
#     """
#     pass
#
#
# def create_kibana(username,password,email):
#     """
#         创建kibana用户
#     :param username:
#     :param password:
#     :param email:
#     :return:
#     """
#     pass
#
#
# def create_zabbix(username,password,phone):
#     """
#         创建zabbix用户
#     :param username:
#     :param password:
#     :param phone:
#     :return:
#     """
#     z = zabbix()
#     params = {'alias': username,
#               'passwd': password}
#     params['usrgrps'] = [{'usrgrpid': '7'}]
#     params['user_medias'] = [
#                                   {'mediatypeid': '1',
#                                    'sendto': phone,
#                                    'active': '0',
#                                    'severity': '63',
#                                    'period': '1-7,00:00-24:00'
#                                   }
#                             ]
#     result = z.getdataZabbix('user.create', params)
#     return result
#
#
# def delete_zabbix(username):
#     """
#         删除zabbix用户
#     :param username:
#     :return:
#     """
#     z = zabbix()
#     params = [z.username_to_id(username)]
#     result = z.getdataZabbix('user.delete', params)
#     return result
#
#
# def check_manage_password(*args):
#     """
#         暂时用于删除业务逻辑
#     :param args:
#     :return:
#     """
#     pass
#
#
# def get_message(request):
#     """
#         获取员工用户，部门和电话
#     :param request:
#     :return:
#     """
#     user_info = User_info.objects.all()
#     return render(request, "getmessage.html", {'user_info': user_info})
#
#
#
#
# def interface_user_phone(request):
#     """
#         ajax接口，用于返回用户，部门和电话
#     :param request:
#     :return:
#     """
#
#     result = {'status': False,
#               'data': []}
#
#     if request.POST.get('searchstr'):
#         pass
#     try:
#         user_info = User_info.objects.all()
#         for i in user_info:
#             result['data'].append({'username':i['username'],'phone':i['phone'],'department':i['department'],})
#         result['status'] = True
#     except:
#         pass
#     return HttpResponse(json.dumps(result))








