# -*- coding: utf-8 -*-
# 2017-12-21
# by why

from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.http import HttpResponse

from opmanage.forms.domain import AddDomainForm, DelDomainForm
from opmanage.models import Domain_info
from opmanage.views.index import check_login, check_user_auth


# 用于判定页面访问权限的下标
check_num = 2

@check_login
@check_user_auth(check_num=check_num)
def add_domain(request):
    """
        添加主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        add_domainform = AddDomainForm(request.POST)
        # 字段验证通过
        if add_domainform.is_valid():
            # 插入数据
            add_domainform.save()
            # 创建域名解析成功
            return HttpResponse('add,domain %s ok' % name)
        # 字段验证不通过
        else:
            return render(request, "domain/adddomain.html", {'add_domainform': add_domainform, 'error': add_domainform.errors})
    # 非POST请求
    else:
        add_domainform = AddDomainForm()
        return render(request, "domain/adddomain.html", {'add_domainform': add_domainform})


@check_login
@check_user_auth(check_num=check_num)
def del_domain(request):
    """
        添加主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        del_domainform = DelDomainForm(request.POST)
        # 字段验证通过
        if del_domainform.is_valid():
            name = request.POST.get('name', None)
            # 删除数据
            Domain_info.objects.filter(name=name).delete()
            # 删除域名解析成功
            return HttpResponse('del,domain %s ok' % name)
        # 字段验证不通过
        else:
            return render(request, "domain/deldomain.html", {'del_domainform': del_domainform, 'error': del_domainform.errors})
    # 非POST请求
    else:
        del_domainform = DelDomainForm()
        return render(request, "domain/deldomain.html", {'del_domainform': del_domainform})