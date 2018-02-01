# -*- coding: utf-8 -*-
# 2017-12-18
# by why


from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.http import HttpResponse


from opmanage.forms.lb import AddLbForm, DelLbForm, UpdataLbForm, GetLbForm
from opmanage.models import Lb_info
from opmanage.views.index import check_login, check_user_auth, to_page
from opmanage.views.host import add_zabbix_host, del_zabbix_host
from workorder.models import Host_WorkOrder_info, Status_WorkOrder_info


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
            return render(request, "opmanage/lb/addlb.html", {'add_lbform': add_lbform})
    # 非POST请求
    else:
        host_workorder_id = request.GET.get('host_workorder_id', None)
        step_num = request.GET.get('step_num', None)
        net = request.GET.get('net', None)
        # intranet
        if host_workorder_id != None:
            host_workorder_obj = Host_WorkOrder_info.objects.filter(host_workorder_id=host_workorder_id).first()
            form = AddLbForm(initial={'host_workorder_id': host_workorder_id,
                                      'net_type': net,
                                      'role': role,
                                      'step_num': step_num,
                                      'serverline': host_workorder_obj.serverline_name,
                                        })
        else:
            form = AddLbForm()
        return render(request, "opmanage/lb/addlb.html", {'add_lbform': form})


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
            # Lb_info.objects.get(lb_name=lb_name).backend_host.clear() clear只删除多对多关系
            Lb_info.objects.get(lb_name=lb_name).delete()
            # 删除zabbix监控
            del_zabbix_host(host=lb_name)
            # 创建用户成功
            return HttpResponse('del lb %s ok' % lb_name)
        # 字段验证不通过
        else:
            return render(request, "opmanage/lb/dellb.html", {'del_lbform': del_lbform})
    # 非POST请求
    else:
        lb_name = request.GET.get('lb_name')
        if lb_name != None:
            del_lbform = DelLbForm({'lb_name': lb_name})
        else:
            del_lbform = DelLbForm()
        return render(request, "opmanage/lb/dellb.html", {'del_lbform': del_lbform})


@check_login
@check_user_auth(check_num=check_num)
def updata_lb(request):
    """
        更新主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        updata_lbform = UpdataLbForm(request.POST)
        # 字段验证通过
        if updata_lbform.is_valid():
            # 添加LB数据
            lb_name = request.POST.get('lb_name', None)
            # cname = request.POST.get('cname', None)
            # ipaddr = request.POST.get('cname', None)
            backend_host = request.POST.get('cname', None)
            role_from_port = request.POST.get('cname', None)
            role_to_port = request.POST.get('cname', None)
            # cloud = request.POST.get('cname', None)
            # types = request.POST.get('cname', None)
            serverline = request.POST.get('cname', None)
            lb = Lb_info.objects.get(lb_name=lb_name)
            updata_lbform = UpdataLbForm(request.POST, instance=lb)
            updata_lbform.save()
            # if role_from_port != lb.role_from_port:
            #     lb.role_from_port = role_from_port
            # if role_to_port != lb.role_to_port:
            #     lb.role_to_port = role_to_port
            # if int(serverline) != lb.serverline.id:
            #     lb.serverline.id = int(serverline)
            # lb.save()
            # lb.backend_host.clear()

            # lb.backend_host.add()


            # 添加LB成功
            return HttpResponse('updata lb %s ok' % lb_name)
        # 字段验证不通过
        else:
            return render(request, "opmanage/lb/updatalb.html", {'updata_lbform': updata_lbform})
    # 非POST请求
    else:
        lb_name = request.GET.get('lb_name')
        if lb_name != None:
            lb = Lb_info.objects.get(lb_name=lb_name)
            # 参考https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#modelform
            updata_lbform = UpdataLbForm(instance=lb)
        else:
            updata_lbform = UpdataLbForm()
        return render(request, "opmanage/lb/updatalb.html", {'updata_lbform': updata_lbform})


@check_login
@check_user_auth(check_num=check_num)
def get_lb(request):
    """
        获取主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        get_lbform = GetLbForm(request.POST)
        # 字段验证通过
        if get_lbform.is_valid():
            lb_name = request.POST.get('lb_name', None)
            every_page_sum = request.POST.get('every_page_sum', 20)
            pages = request.POST.get('pages', 1)
            if lb_name == '' or lb_name == None:
                lb_list = Lb_info.objects.all()
            else:
                lb_list = []
                # lb_list = Lb_info.objects.filter(lb_name=lb_name)
                for i in Lb_info.objects.all():
                    if lb_name in i.lb_name:
                        lb_list.append(i)
            page_lb_list = to_page(lb_list, pages, every_page_sum)
            # 获取相关LB信息
            return render(request, "opmanage/lb/getlb.html", {'get_lbform': get_lbform, 'page_lb_list': page_lb_list})
        # 字段验证不通过
        else:
            return render(request, "opmanage/lb/getlb.html", {'get_lbform': get_lbform})
    # 非POST请求
    else:

        every_page_sum = 20
        # 获取当前页码
        pages = request.GET.get('page') or 1
        # 创建回传前端表单，如果lb_name存在，返回相lb_name表单，否则返回空白表单
        lb_name = request.GET.get('lb_name', None)
        if lb_name == '' or lb_name == None:
            lb_list = Lb_info.objects.all()
            get_lbform = GetLbForm()
        else:
            lb_list = []
            for i in Lb_info.objects.all():
                if lb_name in i.lb_name:
                    lb_list.append(i)
            get_lbform = GetLbForm({'lb_name': lb_name})
        page_lb_list = to_page(lb_list, pages, every_page_sum)
        return render(request, "opmanage/lb/getlb.html", {'get_lbform': get_lbform, 'page_lb_list': page_lb_list})


