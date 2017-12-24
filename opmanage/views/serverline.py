# -*- coding: utf-8 -*-
# 2017-12-24
# by why


import time
import json
from django.shortcuts import render,render_to_response,HttpResponseRedirect,redirect
from django.http import HttpResponse

from opmanage.views.index import check_login, check_user_auth
from opmanage.forms.serverline import AddServerlineForm, DelServerlineForm
from opmanage.models import Serverline_info


# 用于判定页面访问权限的下标
check_num = 1

# @check_login
# @check_user_auth(check_num=check_num)
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
            return render(request, "serverline/addserverline.html", {'add_serverlineform': add_serverlineform, 'error': add_serverlineform.errors})
    # 非POST请求
    else:
        add_serverlineform = AddServerlineForm()
        return render(request,"serverline/addserverline.html", {'add_serverlineform': add_serverlineform})


# @check_login
# @check_user_auth(check_num=check_num)
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
            serverline_name = request.POST.get('serverline_name', None)
            Serverline_info.objects.filter(serverline_name=serverline_name).delete()
            return HttpResponse('ok')
        # 字段验证不通过
        else:
            return render(request, "serverline/delserverline.html", {'del_serverlineform': del_serverlineform, 'error': del_serverlineform.errors})
    # 非POST请求
    else:
        del_serverlineform = DelServerlineForm()
        return render(request,"serverline/delserverline.html", {'del_serverlineform': del_serverlineform})
