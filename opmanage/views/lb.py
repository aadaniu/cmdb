# -*- coding: utf-8 -*-
# 2017-12-18
# by why


from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from opmanage.forms.lb import AddLbForm, DelLbForm, UpdataLbForm, GetLbForm
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
            return render(request, "lb/addlb.html", {'add_lbform': add_lbform})
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
            return render(request, "lb/dellb.html", {'del_lbform': del_lbform})
    # 非POST请求
    else:
        del_lbform = DelLbForm()
        return render(request, "lb/dellb.html", {'del_lbform': del_lbform})


@check_login
@check_user_auth(check_num=check_num)
def updata_lb(request):
    """
        添加主机
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
            print lb_name
            Lb_info.objects.get(lb_name=lb_name)
            updata_lbform.save()
            # 添加LB成功
            return HttpResponse('updata lb %s ok') % lb_name
        # 字段验证不通过
        else:
            return render(request, "lb/updatalb.html", {'updata_lbform': updata_lbform})
    # 非POST请求
    else:
        lb_name = request.GET.get('lb_name')
        if lb_name != None:
            lb = Lb_info.objects.get(lb_name=lb_name)
            # 参考https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#modelform
            updata_lbform = UpdataLbForm(instance=lb)
        else:
            updata_lbform = UpdataLbForm()
        return render(request, "lb/updatalb.html", {'updata_lbform': updata_lbform})


@check_user_auth(check_num=check_num)
def get_lb(request):
    """
        添加主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        get_lbform = GetLbForm(request.POST)
        # 字段验证通过
        if get_lbform.is_valid():
            search_lb = request.POST.get('search_lb', None)
            every_page_sum = request.POST.get('every_page_sum', 20)
            pages = request.POST.get('pages', 1)
            if search_lb == '' or search_lb == None:
                lb_list = Lb_info.objects.all()
            else:
                lb_list = []
                # lb_list = Lb_info.objects.filter(lb_name=search_lb)
                for i in Lb_info.objects.all():
                    if search_lb in i.lb_name:
                        lb_list.append(i)
            page_lb_list = to_page(lb_list, pages, every_page_sum)
            # 获取相关LB信息
            return render(request, "lb/getlb.html", {'get_lbform': get_lbform, 'page_lb_list': page_lb_list})
        # 字段验证不通过
        else:
            return render(request, "lb/addlb.html", {'get_lbform': get_lbform})
    # 非POST请求
    else:

        every_page_sum = 20
        # 获取当前页码
        pages = request.GET.get('page') or 1
        # 创建回传前端表单，如果search_lb存在，返回相search_lb表单，否则返回空白表单
        search_lb = request.GET.get('search_lb', None)
        if search_lb == '' or search_lb == None:
            lb_list = Lb_info.objects.all()
            get_lbform = GetLbForm()
        else:
            lb_list = []
            for i in Lb_info.objects.all():
                if search_lb in i.lb_name:
                    lb_list.append(i)
            get_lbform = GetLbForm({'search_lb': search_lb})
        page_lb_list = to_page(lb_list, pages, every_page_sum)
        return render(request, "lb/getlb.html", {'get_lbform': get_lbform, 'page_lb_list': page_lb_list})


def to_page(list, pages, every_page_sum):
    """
        构造分页
    :param list: 列表
    :param pages:  当前页数
    :param every_page_sum: 每页显示数量
    :return:
    """
    paginator = Paginator(list, every_page_sum)
    try:
        page_list = paginator.page(pages)
    except PageNotAnInteger:
        page_list = paginator.page(1)
    except EmptyPage:
        page_list = paginator.page(paginator.num_pages)
    return page_list