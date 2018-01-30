# -*- coding: utf-8 -*-
# 2017-11-29
# by why

import time
from django.shortcuts import render,render_to_response,HttpResponseRedirect,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from opmanage.forms.index import LoginUserForm, LockScreenUserForm
from opmanage.models import User_info, Notice_info, Show_info



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
        elif request.session.get('login_status', None) == 2:
            return redirect('/index/lock_screen/')
        else:
            # print 'check_login验证登录状态不通过，跳转到登录页面no'
            return redirect('/index/login/?nextpath=%s'% request.path)

    return check_login_status

def check_user_auth(check_num):
    """
        装饰器，用于检测用户页面访问权限
    :param func:
    :param check_num: 权限认证级别，1为admin，2为op， 3为other
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
                username = request.session.get('username')
                # 添加session
                request.session['path_info'] = request.META.get('PATH_INFO')

                # 用于返回消息和展示
                notice = load_message(username)
                show = load_show(username)
                return func(request, notice, show, *args)
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


@check_login
@check_user_auth(check_num=3)
def index(request, notice=None, show=None):
    """
        浏览主页
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'opmanage/index/index.html', locals())


def logout(request):
    """
        用于用户退出
    :param request:
    :return:
    """
    request.session.set_expiry(0.1)
    time.sleep(0.2)
    return redirect('opmanage/index/login/')


@csrf_protect
def lock_screen(request):
    """
        用于锁屏
    :param request:
    :return:
    """
    login_status = request.session.get('login_status',None)
    if login_status == None:
        return redirect('opmanage/index/login/')
    else:
        if request.method == 'GET':
            request.session['login_status'] = 2
            userform = LockScreenUserForm()
            return render(request, "opmanage/index/lock_screen.html",{'userform': userform})
        elif request.method == 'POST':
            userform = LockScreenUserForm(request.POST)
            # 字段验证通过
            if userform.is_valid():
                username = request.POST.get('username')
                # 如果有没有post数据，则
                if len(username) == 0 or username == None:
                    username = request.session.get('username', None)
                password = request.POST.get('password')
                if User_info.objects.filter(username=username,password=password).count():
                    # 添加session
                    request.session['username'] = username
                    request.session['auth'] = get_auth(username)
                    request.session['login_status'] = 1
                    return redirect('/index/index/')
                else:
                    userform.errors['password'] = ['password error',]
                    print userform
                    return render(request, "opmanage/index/lock_screen.html", {'userform': userform})
            # 字段验证不通过
            else:
                return render(request, "opmanage/index/lock_screen.html", {'userform': userform})





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

    return User_info.objects.filter(username=username).values('notice_info__notice_type','notice_info__subject','notice_info__link_url')


def load_show(username=None):
    """
        用于返回前端
    :param username:
    :return:
    """
    return Show_info.objects.filter(username__username=username).first()


def check_op(request):
    """
        用于检测是否为运维
    :param reuest:
    :return:
    """
    if int(request.session.get('auth')) <= 2:
        return True
    else:
        return False





