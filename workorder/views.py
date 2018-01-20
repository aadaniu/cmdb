# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.http import HttpResponse
from django.db.models import Q


from workorder.forms import *
from opmanage.views.index import check_login, check_user_auth, to_page, load_message
from opmanage.models import User_info, Notice_info
from opmanage.models import Serverline_info


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
            return render(request, "workorder/serverline_workorder.html", {'form': form})

    # 非POST请求
    else:
        form = AddServerlineWorkOrderForm()
        return render(request, "workorder/serverline_workorder.html", {'form': form})

@check_login
@check_user_auth(check_num=check_num)
def add_host_workorder(request):
    """
        添加主机工单
    :param request:
    :return:
    """
    # POST请求
    request_user = request.session.get('username')
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
            work_order.submit_user = request_user
            work_order.save()
            # 用户构造
            url = '/workorder/check_host_workorder/?id=%s' % work_order.id
            op_admin = User_info.objects.get(username='cmdbadmin')
            Notice_info.objects.create(username_id=op_admin.id, notice_type='WorkOrder', subject=work_order.subject, link_url=url)
            return HttpResponse('add,work order ok')

        # 字段验证不通过
        else:
            return render(request, "workorder/host_workorder.html", {'form': form, 'notice': load_message(request_user)})

    # 非POST请求
    else:
        form = AddHostWorkOrderForm()
        return render(request, "workorder/host_workorder.html", {'form': form, 'notice': load_message(request_user)})


@check_login
@check_user_auth(check_num=check_num)
def check_host_workorder(request):
    """
        运维审核主机工单
    :param request:
    :return:
    """
    request_user = request.session.get('username')
    # POST请求
    if request.method == "POST":
        form = AddHostWorkOrderForm(request.POST)
        # 字段验证通过
        if form.is_valid():
            # 插入数据
            work_order = form.save(commit=False)
            work_order.submit_user = request.session.get('username')
            work_order.save()
            return HttpResponse('add,work order ok')

        # 字段验证不通过
        else:
            return render(request, "workorder/host_workorder.html", {'form': form})

    # 非POST请求
    else:
        url = request.META.get('PATH_INFO')
        id = request.GET.get('id')
        link_url = '%s?id=%s' % (url, id)
        print Notice_info.objects.filter(Q(username__username='cmdbadmin')&Q(link_url=link_url)).delete()
        host_workorder = Host_WorkOrder_info.objects.get(id=id)
        form = AddHostWorkOrderForm(instance=host_workorder)
        return render(request, "workorder/host_workorder_check.html", {'form': form})


