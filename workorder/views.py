# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,render_to_response,HttpResponseRedirect,redirect
from django.http import HttpResponse
from django.db.models import Q


from workorder.forms import *
from workorder.models import *
from opmanage.views.index import check_login, check_user_auth, to_page, load_message, load_show
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
def add_host_workorder(request, notice=None, show=None):
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
            host_workorder_obj = form.save(commit=False)
            host_workorder_obj.submit_user = request_user
            host_workorder_obj.save()

            # 添加步骤1
            status_workorder_obj = Status_WorkOrder_info.objects.create(step_num='step1', step_message='%s提交工单成功' % host_workorder_obj.subject, step_status='ok')
            status_workorder_obj.attribute_workorder.add(host_workorder_obj)
            # 用户构造
            url = '/workorder/check_host_workorder/?host_workorder_id=%s' % host_workorder_obj.host_workorder_id
            user_opadmin_object = User_info.objects.get(username='cmdbadmin')
            Notice_info.objects.create(username_id=user_opadmin_object.id, notice_type='WorkOrder', subject=host_workorder_obj.subject, link_url=url)
            # 添加步骤2
            status_workorder_obj = Status_WorkOrder_info.objects.create(step_num='step2', step_message='运维审核工单', step_url=url)
            status_workorder_obj.attribute_workorder.add(host_workorder_obj)
            return redirect('/workorder/get_host_workorder/?host_workorder_id=host_workorder_obj', locals())

        # 字段验证不通过
        else:
            return render(request, "workorder/add_host_workorder.html", locals())

    # 非POST请求
    else:
        form = AddHostWorkOrderForm()
        return render(request, "workorder/add_host_workorder.html", {'form': form, 'notice': notice, 'show': show})


@check_login
@check_user_auth(check_num=check_num)
def check_host_workorder(request, notice=None, show=None):
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
            # 更新数据
            subject = request.POST.get('subject', None)
            host_workorder_obj = Host_WorkOrder_info.objects.get(subject=subject)
            a = AddHostWorkOrderForm(request.POST, instance=host_workorder_obj)
            a.save()
            # 更新步骤2
            status_workorder_obj = Status_WorkOrder_info.objects.filter(Q(step_num='step2')&Q(attribute_workorder__host_workorder_id=host_workorder_obj.host_workorder_id)).first()
            status_workorder_obj.step_status = 'ok'
            status_workorder_obj.save()
            return HttpResponse('add,work order ok')

        # 字段验证不通过
        else:
            return render(request, "workorder/check_host_workorder.html", {'form': form, 'notice': notice, 'show': show})

    # 非POST请求
    else:
        url = request.META.get('PATH_INFO')
        host_workorder_id = request.GET.get('host_workorder_id')
        link_url = '%s?host_workorder_id=%s' % (url, host_workorder_id)
        # 更新Notice信息
        Notice_info.objects.filter(Q(username__username='cmdbadmin')&Q(link_url=link_url)).delete()
        # 更新
        host_workorder_obj = Host_WorkOrder_info.objects.get(host_workorder_id=host_workorder_id)
        form = AddHostWorkOrderForm(instance=host_workorder_obj)
        return render(request, "workorder/check_host_workorder.html", {'form': form, 'notice': notice, 'show': show})



@check_login
@check_user_auth(check_num=check_num)
def get_host_workorder(request, notice=None, show=None):
    """
        获取主机工单
    :param request:
    :return:
    """
    request_user = request.session.get('username')
    form = Host_WorkOrder_info.objects.filter(submit_user=request_user).all()
    return render(request, "workorder/get_host_workorder.html", {'form': form, 'notice': notice, 'show': show})


@check_login
@check_user_auth(check_num=check_num)
def status_host_workorder(request, notice=None, show=None):
    """
        获取主机工单状态
    :param request:
    :return:
    """
    host_workorder_id = request.GET.get('host_workorder_id')
    form = Status_WorkOrder_info.objects.filter(attribute_workorder__host_workorder_id=host_workorder_id).all().order_by('-step_num')
    return render(request, "workorder/status_host_workorder.html", {'form': form, 'notice': notice, 'show': show})


def exec_workorder(request, notice=None, show=None):
    """
        执行工单
    :param request:
    :param notice:
    :param show:
    :return:
    """
    host_workorder_id = request.GET.get('host_workorder_id')
    host_workorder_obj = Host_WorkOrder_info.objects.get(host_workorder_id=host_workorder_id)
    # 根据工单设计操作url
    step = 2
    # host
    step += 1
    Status_WorkOrder_info.objects.create(host_workorder_id=host_workorder_id,
                                         step_num='step%s' % step,
                                         step_message='创建主机',
                                         step_url='host/addhost/host_workorder_id=%s' % host_workorder_id)
    # elb
    if host_workorder_obj.internal_lb == 't':
        step += 1
        Status_WorkOrder_info.objects.create(step_num='step%s' % step,
                                             step_message='创建内网ELB',
                                             step_url='lb/addlb/host_workorder_id=%s&' % host_workorder_id)
    if host_workorder_obj.internet_facing_lb == 't':
        step += 1
        Status_WorkOrder_info.objects.create(step_num='step%s' % step,
                                             step_message='创建外网ELB',
                                             step_url='lb/addlb/host_workorder_id=%s&' % host_workorder_id)
    # domain
    if host_workorder_obj.internal_domain == 't':
        step += 1
        Status_WorkOrder_info.objects.create(step_num='step%s' % step,
                                             step_message='创建内网域名',
                                             step_url='domain/adddomain/host_workorder_id=%s' % host_workorder_id)
    if host_workorder_obj.internet_facing_domain == 't':
        step += 1
        status_workorder_obj = Status_WorkOrder_info.objects.create(step_num='step%s' % step, step_message='创建外域名',step_url='domain/adddomain/host_workorder_id=%s' % host_workorder_id)
    # env
    step += 1
    status_workorder_obj = Status_WorkOrder_info.objects.create(step_num='step%s' % step, step_message='生成正式环境')
    # monitor
    step += 1
    status_workorder_obj = Status_WorkOrder_info.objects.create(step_num='step%s' % step, step_message='添加监控')
    # log
    step += 1
    status_workorder_obj = Status_WorkOrder_info.objects.create(step_num='step%s' % step, step_message='配置日志切分，保存和上传')




    return render(request, "workorder/status_host_workorder.html", {'host_workorder_obj': host_workorder_obj, 'notice': notice, 'show': show})
