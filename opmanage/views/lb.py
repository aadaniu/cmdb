# -*- coding: utf-8 -*-
# 2017-12-18
# by why


from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.http import HttpResponse

from opmanage.forms.lb import AddLbForm, DelLbForm
from opmanage.models import Lb_info
from opmanage.views.index import check_login, check_user_auth
from opmanage.views.host import add_zabbix_host, del_zabbix_host


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
            # 添加LB数据
            add_lbform.save()
            # 添加zabbix监控
            lb_name = request.POST.get('lb_name', None)
            zabbix_proxy_id = '127.0.0.1'
            add_zabbix_host(host=lb_name, ip=zabbix_proxy_id)
            # 添加LB成功
            return HttpResponse('add lb %s ok' % lb_name)
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
            lb_name = request.POST.get('lb_name', None)
            # 删除数据
            Lb_info.objects.filter(name=lb_name).delete()
            # 删除zabbix监控
            del_zabbix_host(host=lb_name)
            # 创建用户成功
            return HttpResponse('del lb %s ok' % lb_name)
        # 字段验证不通过
        else:
            return render(request, "lb/dellb.html", {'del_lbform': del_lbform, 'error': del_lbform.errors})
    # 非POST请求
    else:
        del_lbform = DelLbForm()
        return render(request, "lb/dellb.html", {'del_lbform': del_lbform})