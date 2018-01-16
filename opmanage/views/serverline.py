# -*- coding: utf-8 -*-
# 2017-12-24
# by why


import time
import json
from django.shortcuts import render,render_to_response,HttpResponseRedirect,redirect
from django.http import HttpResponse

from opmanage.views.index import check_login, check_user_auth, to_page
from opmanage.forms.serverline import *
from opmanage.models import *


# 用于判定页面访问权限的下标
check_num = 1

@check_login
@check_user_auth(check_num=check_num)
def add_serverline(request):
    """
        添加部门
    :param request:
    :return:
    """
    # post请求
    if request.method == "POST":
        add_serverlineform = AddServerlineForm(request.POST)
        # 字段验证通过
        if add_serverlineform.is_valid():
            add_serverlineform.save()
            return HttpResponse('ok')
        # 字段验证不通过
        else:
            return render(request, "opmanage/serverline/addserverline.html", {'add_serverlineform': add_serverlineform, 'error': add_serverlineform.errors})
    # 非POST请求
    else:
        add_serverlineform = AddServerlineForm()
        return render(request,"opmanage/serverline/addserverline.html", {'add_serverlineform': add_serverlineform})


@check_login
@check_user_auth(check_num=check_num)
def del_serverline(request):
    """
        添加部门
    :param request:
    :return:
    """
    # post请求
    if request.method == "POST":
        del_serverlineform = DelServerlineForm(request.POST)
        # 字段验证通过
        if del_serverlineform.is_valid():
            # 获取需要删除的业务线
            serverline_name = request.POST.get('serverline_name', None)
            # 查找对应业务线对象
            serverline = Serverline_info.objects.get(serverline_name=serverline_name)
            # 删除serverline前先更改serverline下主机，域名，LB的业务线为no_serverline
            for i in serverline.host_info_set.all():
                print i.host_name
                print i.serverline_id
                i.serverline_id = Serverline_info.objects.get(serverline_name='no_serverline').id
                print i.serverline_id
                i.save()
            # 删除业务线
            serverline.delete()
            return HttpResponse('ok')
        # 字段验证不通过
        else:
            return render(request, "opmanage/serverline/delserverline.html", {'del_serverlineform': del_serverlineform, 'error': del_serverlineform.errors})
    # 非POST请求
    else:
        serverline_name = request.GET.get('serverline_name')
        if serverline_name != None:
            del_serverlineform = DelServerlineForm({'serverline_name': serverline_name})
        else:
            del_serverlineform = DelServerlineForm()
        return render(request,"opmanage/serverline/delserverline.html", {'del_serverlineform': del_serverlineform})



@check_login
@check_user_auth(check_num=check_num)
def updata_serverline(request):
    """
        更新主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        updata_serverlineform = UpdataServerlineForm(request.POST)
        # 字段验证通过
        if updata_serverlineform.is_valid():
            # 更新业务线数据
            serverline_name = request.POST.get('serverline_name', None)
            serverline = Serverline_info.objects.get(serverline_name=serverline_name)
            updata_serverlineform = UpdataServerlineForm(request.POST, instance=serverline)
            updata_serverlineform.save()
            # 更新业务线数据成功
            return HttpResponse('updata serverline %s ok' % serverline_name)
        # 字段验证不通过
        else:
            return render(request, "opmanage/serverline/updataserverline.html", {'updata_serverlineform': updata_serverlineform})
    # 非POST请求
    else:
        serverline_name = request.GET.get('serverline_name')
        if serverline_name != None:
            serverline = Serverline_info.objects.get(serverline_name=serverline_name)
            # 初始化表单
            # 参考https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#modelform
            updata_serverlineform = UpdataServerlineForm(instance=serverline)
        else:
            updata_serverlineform = UpdataServerlineForm()
        return render(request, "opmanage/serverline/updataserverline.html", {'updata_serverlineform': updata_serverlineform})


@check_login
@check_user_auth(check_num=check_num)
def get_serverline(request):
    """
        获取主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        get_serverlineform = GetServerlineForm(request.POST)
        # 字段验证通过
        if get_serverlineform.is_valid():
            serverline_name = request.POST.get('serverline_name', None)
            every_page_sum = request.POST.get('every_page_sum', 20)
            pages = request.POST.get('pages', 1)
            if serverline_name == '' or serverline_name == None:
                serverline_list = Serverline_info.objects.all()
            else:
                serverline_list = []
                for i in Serverline_info.objects.all():
                    if serverline_name in i.serverline_name:
                        serverline_list.append(i)
            page_serverline_list = to_page(serverline_list, pages, every_page_sum)
            # 获取相关业务线信息
            return render(request, "opmanage/serverline/getserverline.html", {'get_serverlineform': get_serverlineform, 'page_serverline_list': page_serverline_list})
        # 字段验证不通过
        else:
            return render(request, "opmanage/serverline/getserverline.html", {'get_serverlineform': get_serverlineform})
    # 非POST请求
    else:
        every_page_sum = 20
        # 获取当前页码
        pages = request.GET.get('page') or 1
        serverline_name = request.GET.get('serverline_name', None)
        # 创建回传前端表单，如果serverline_name存在，返回serverline_name相关表单，否则返回空白表单
        if serverline_name == '' or serverline_name == None:
            serverline_list = Serverline_info.objects.all()
            get_serverlineform = GetServerlineForm()
        else:
            serverline_list = []
            for i in Serverline_info.objects.all():
                if serverline_name in i.serverline_name:
                    serverline_list.append(i)
            get_serverlineform = GetServerlineForm({'serverline_name': serverline_name})
        page_serverline_list = to_page(serverline_list, pages, every_page_sum)
        return render(request, "opmanage/serverline/getserverline.html", {'get_serverlineform': get_serverlineform, 'page_serverline_list': page_serverline_list})

