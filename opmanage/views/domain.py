# -*- coding: utf-8 -*-
# 2017-12-21
# by why

from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.http import HttpResponse
from django.db.models import Q

from opmanage.forms.domain import *
from opmanage.models import Domain_info
from opmanage.views.index import check_login, check_user_auth, to_page
from workorder.models import Host_WorkOrder_info, Status_WorkOrder_info
from workorder.views import step_status_ok


# 用于判定页面访问权限的下标
check_num = 2

@check_login
@check_user_auth(check_num=check_num)
def add_domain(request, notice=None, show=None):
    """
        添加主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        form = AddDomainForm(request.POST)
        # 字段验证通过
        if form.is_valid():
            host_workorder_id = request.POST.get('host_workorder_id')
            step_num = request.POST.get('step_num')
            net_type = request.POST.get('net_type')
            domain = request.POST.get('domain')
            serverline = request.POST.get('serverline')
            # 创建LB
            create_domain(net_type, domain, serverline)

            # 添加zabbix监控
            # zabbix_proxy_id = '127.0.0.1'
            # add_zabbix_host(host=lb_name, ip=zabbix_proxy_id)

            func_status = step_status_ok(host_workorder_id, step_num)
            if func_status:
                # 创建主机成功
                return HttpResponse('add host ok')
            else:
                return HttpResponse('add host false')
        # 字段验证不通过
        else:
            return render(request, "opmanage/domain/adddomain.html", locals())
    # 非POST请求
    else:
        host_workorder_id = request.GET.get('host_workorder_id', None)
        step_num = request.GET.get('step_num', None)
        net = request.GET.get('net', None)
        domain = request.GET.get('domain', None)
        # intranet
        if host_workorder_id != None:
            host_workorder_obj = Host_WorkOrder_info.objects.filter(host_workorder_id=host_workorder_id).first()

            form = AddDomainForm(initial={'host_workorder_id': host_workorder_id,
                                          'net_type': net,
                                          'domain': domain,
                                          'step_num': step_num,
                                          'serverline': host_workorder_obj.serverline_name,
                                          })
        else:
            form = AddDomainForm()
        return render(request, "opmanage/domain/adddomain.html", {'form': form, 'notice': notice, 'show': show})


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
            domain = request.POST.get('domain', None)
            q = Q()
            q.connector = 'AND'
            q.children.append(('name', name))
            q.children.append(('domain', domain))
            # 删除数据
            Domain_info.objects.filter(q).delete()
            # 删除域名解析成功
            return HttpResponse('del,domain %s@%s ok' % (name,domain))
        # 字段验证不通过
        else:
            return render(request, "opmanage/domain/deldomain.html", {'del_domainform': del_domainform, 'error': del_domainform.errors})
    # 非POST请求
    else:
        name = request.GET.get('name')
        domain = request.GET.get('domain')
        if name != None and domain != None:
            del_domainform = DelDomainForm({'name': name, 'domain': domain})
        else:
            del_domainform = DelDomainForm()
        return render(request, "opmanage/domain/deldomain.html", {'del_domainform': del_domainform})



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
            return render(request, "opmanage/domain/updatadomain.html", {'updata_domainform': updata_domainform})
    # 非POST请求
    else:
        name = request.GET.get('name')
        domain = request.GET.get('domain')
        if name != None and domain != None:
            q = Q()
            q.connector = 'AND'
            q.children.append(('name', name))
            q.children.append(('domain', domain))
            domain = Domain_info.objects.get(q)
            # 参考https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#modelform
            updata_domainform = UpdataDomainForm(instance=domain)
        else:
            updata_domainform = UpdataDomainForm()
        return render(request, "opmanage/domain/updatadomain.html", {'updata_domainform': updata_domainform})


@check_login
@check_user_auth(check_num=check_num)
def get_domain(request):
    """
        获取主机
    :param request:
    :return:u
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
            return render(request, "opmanage/domain/getdomain.html", {'get_domainform': get_domainform, 'page_domain_list': page_domain_list})
        # 字段验证不通过
        else:
            return render(request, "opmanage/domain/getdomain.html", {'get_domainform': get_domainform})
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
        return render(request, "opmanage/domain/getdomain.html", {'get_domainform': get_domainform, 'page_domain_list': page_domain_list})


def create_domain(net_type, domain, serverline):
    """
        添加外网域名解析
    :param net_type:
    :param domain:
    :param serverline:
    :return:
    """
    pass


