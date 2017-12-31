# -*- coding: utf-8 -*-
# 2017-12-21
# by why

from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.http import HttpResponse

from opmanage.forms.domain import *
from opmanage.models import Domain_info
from opmanage.views.index import check_login, check_user_auth, to_page


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
            return HttpResponse('add,domain ok')
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



@check_login
@check_user_auth(check_num=check_num)
def updata_domain(request):
    """
        更新主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        updata_domainform = UpdataDomainForm(request.POST)
        # 字段验证通过
        if updata_domainform.is_valid():
            # 添加domain数据
            name = request.POST.get('name', None)
            domain = Domain_info.objects.get(name=name)
            updata_domainform = UpdataDomainForm(request.POST, instance=domain)
            updata_domainform.save()
            # 添加domain成功
            return HttpResponse('updata domain %s ok' % name)
        # 字段验证不通过
        else:
            return render(request, "domain/updatadomain.html", {'updata_domainform': updata_domainform})
    # 非POST请求
    else:
        name = request.GET.get('name')
        if name != None:
            domain = Domain_info.objects.get(name=name)
            # 参考https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#modelform
            updata_domainform = UpdataDomainForm(instance=domain)
        else:
            updata_domainform = UpdataDomainForm()
        return render(request, "domain/updatadomain.html", {'updata_domainform': updata_domainform})


@check_login
@check_user_auth(check_num=check_num)
def get_domain(request):
    """
        获取主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        get_domainform = GetDomainForm(request.POST)
        # 字段验证通过
        if get_domainform.is_valid():
            name = request.POST.get('name', None)
            every_page_sum = request.POST.get('every_page_sum', 20)
            pages = request.POST.get('pages', 1)
            if name == '' or name == None:
                domain_list = Domain_info.objects.all()
            else:
                domain_list = []
                for i in Domain_info.objects.all():
                    if name in i.name:
                        domain_list.append(i)
            page_domain_list = to_page(domain_list, pages, every_page_sum)
            # 获取相关domain信息
            return render(request, "domain/getdomain.html", {'get_domainform': get_domainform, 'page_domain_list': page_domain_list})
        # 字段验证不通过
        else:
            return render(request, "domain/getdomain.html", {'get_domainform': get_domainform})
    # 非POST请求
    else:

        every_page_sum = 20
        # 获取当前页码
        pages = request.GET.get('page') or 1
        # 创建回传前端表单，如果domain存在，返回相domain表单，否则返回空白表单
        name = request.GET.get('name', None)
        if name == '' or name == None:
            domain_list = Domain_info.objects.all()
            get_domainform = GetDomainForm()
        else:
            domain_list = []
            for i in Domain_info.objects.all():
                if name in i.name:
                    domain_list.append(i)
            get_domainform = GetDomainForm({'name': name})
        page_domain_list = to_page(domain_list, pages, every_page_sum)
        return render(request, "domain/getdomain.html", {'get_domainform': get_domainform, 'page_domain_list': page_domain_list})


