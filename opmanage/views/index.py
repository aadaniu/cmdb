# -*- coding: utf-8 -*-
# 2017-11-29
# by why

import time
from django.shortcuts import render,render_to_response,HttpResponseRedirect,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from opmanage.forms.index import LoginUserForm
from opmanage.models import User_info


def check_login(func):
    """
        装饰器，用于判定登录状态
    :param func:
    :return:
    """
    def check_login_status(request, *args):
        # print 'check_login装饰器'
        # 验证登录状态通过，正常显示
        if request.session.get('login_status', None) == 1:
            # print 'check_login验证登录状态通过，正常显示ok'
            r = func(request, *args)
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
        def check_user_auth_2(request, *args):
            # print 'check_user_auth'
            # 取负用作下标
            # 不懂为什么这里写check_num -= 0不行，必须传递给一个变量才能实现。
            local_check_num = int(check_num)
            #local_check_num = 0 - local_check_num
            auth = request.session.get('auth')
            # 验证权限通过
            # if str(auth)[local_check_num] == '1':
            if int(auth) <= local_check_num:
                # print 'check_user_auth验证权限通过ok'
                return func(request, *args)
            else:
                # print 'check_user_auth验证权限不通过no'
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
            return render(request, "opmanage/index/login.html", {'userform': userform, 'error': userform.errors})
    # 非POST请求
    else:
        # 获取登录前要访问的url
        nextpath = request.GET.get('nextpath') or '/index/index/'
        userform = LoginUserForm({'nextpath': nextpath})
        return render(request, "opmanage/index/login.html", {'userform': userform})


def index(request):
    """
        浏览主页
    :param request:
    :return:
    """
    return render(request, 'opmanage/index/index.html')


def logout(request):
    """
        用于用户退出
    :param request:
    :return:
    """
    request.session.set_expiry(0.1)
    time.sleep(0.2)
    return redirect('opmanage/index/login/')


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



def to_page(list, pages, every_page_sum):
    """
        构造分页
    :param list: 列表
    :param pages:  当前页数
    :param every_page_sum: 每页显示数量
    :return:
    """
    paginator = Paginator(list, every_page_sum)
    try:
        page_list = paginator.page(pages)
    except PageNotAnInteger:
        page_list = paginator.page(1)
    except EmptyPage:
        page_list = paginator.page(paginator.num_pages)
    return page_list


def load_message(username=None):
    """
        用于页面间传递message
    :param username:
    :return:
    """
    # 获取当前用户的notice
    username = 'cmdbadmin'
    return HttpResponse(User_info.objects.filter(username='cmdbadmin').values('notice_info__notice_type','notice_info__subject','notice_info__link_url')
)




