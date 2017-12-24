# -*- coding: utf-8 -*-
# 2017-12-18
# by why


from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.http import HttpResponse

from opmanage.forms.lb import AddLbForm, DelLbForm
from opmanage.models import Lb_info
from opmanage.views.index import check_login, check_user_auth
from opmanage.views.host import add_zabbix_host, del_zabbix_host
from lib.zabbix import zabbix

# 用于判定页面访问权限的下标
check_num = 2

@check_login
@check_user_auth(check_num=check_num)
def add_lb(request):
    """
        添加主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        add_lbform = AddLbForm(request.POST)
        # 字段验证通过
        if add_lbform.is_valid():
            name = request.POST.get('name', None)
            cname = request.POST.get('cname', None)
            backend_host = request.POST.get('backend_host', None)
            role_from_port = request.POST.get('role_from_port', None)
            role_to_port = request.POST.get('role_to_port', None)
            ipaddr = request.POST.get('ipaddr', None)
            cloud = request.POST.get('cloud', None)
            types = request.POST.get('types', None)

            # 插入数据
            Lb_info.objects.create(name=name, cname=cname, backend_host=backend_host, role_from_port=role_from_port, role_to_port=role_to_port,
                                   ipaddr=ipaddr, cloud=cloud, types=types)

            # 添加zabbix监控
            zabbix_proxy_id = '127.0.0.1'
            add_zabbix_host(host=name, ip=zabbix_proxy_id)

            # 创建用户成功
            return HttpResponse('add lb %s ok' % name)

        # 字段验证不通过
        else:
            return render(request, "lb/addlb.html", {'add_lbform': add_lbform, 'error': add_lbform.errors})

    # 非POST请求
    else:
        add_lbform = AddLbForm()
        return render(request, "lb/addlb.html", {'add_lbform': add_lbform})


@check_login
@check_user_auth(check_num=check_num)
def del_lb(request):
    """
        删除主机
    :param requets:
    :return:
    """
    # POST请求
    if request.method == "POST":
        del_lbform = DelLbForm(request.POST)
        # 字段验证通过
        if del_lbform.is_valid():
            name = request.POST.get('name', None)

            # 插入数据
            Lb_info.objects.filter(name=name).delete()

            # 添加zabbix监控
            del_zabbix_host(host=name)

            # 创建用户成功
            return HttpResponse('del lb %s ok' % name)

        # 字段验证不通过
        else:
            return render(request, "lb/dellb.html", {'del_lbform': del_lbform, 'error': del_lbform.errors})

    # 非POST请求
    else:
        del_lbform = DelLbForm()
        return render(request, "lb/dellb.html", {'del_lbform': del_lbform})