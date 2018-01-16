# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.http import HttpResponse


from workorder.forms import *
from opmanage.views.index import check_login, check_user_auth, to_page


# 用于判定页面访问权限的下标
check_num = 2


@check_login
@check_user_auth(check_num=check_num)
def add_serverline_workorder(request):
    """
        添加业务线工单
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        form = AddServerlineWorkOrderForm(request.POST)
        # 字段验证通过
        if form.is_valid():
            # 插入数据
            work_order = form.save(commit=False)
            work_order.submit_user = request.session.get('username')
            work_order.save()
            return HttpResponse('add,work order ok')

        # 字段验证不通过
        else:
            return render(request, "host/addhost.html", {'form': form})

    # 非POST请求
    else:
        form = AddHostWorkOrderForm()
        return render(request, "host/addhost.html", {'form': form})

@check_login
@check_user_auth(check_num=check_num)
def add_host_workorder(request):
    """
        添加主机工单
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        form = AddHostWorkOrderForm(request.POST)
        # 字段验证通过
        if form.is_valid():
            """
            https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/
            form = PartialAuthorForm(request.POST)
            author = form.save(commit=False)
            author.title = 'Mr'
            author.save()
            or
            author = Author(title='Mr')
            form = PartialAuthorForm(request.POST, instance=author)
            form.save()
            """
            # 插入数据
            work_order = form.save(commit=False)
            work_order.submit_user = request.session.get('username')
            work_order.save()
            return HttpResponse('add,work order ok')

        # 字段验证不通过
        else:
            return render(request, "host/addhost.html", {'form': form})

    # 非POST请求
    else:
        form = AddHostWorkOrderForm()
        return render(request, "host/addhost.html", {'form': form})


@check_login
@check_user_auth(check_num=check_num)
def check_serverline_workorder(request):
    """
        运维审核主机工单
    :param request:
    :return:
    """
    pass


