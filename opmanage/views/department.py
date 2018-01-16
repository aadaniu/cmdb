# -*- coding: utf-8 -*-
# 2017-12-24
# by why

import time
import json
from django.shortcuts import render,render_to_response,HttpResponseRedirect,redirect
from django.http import HttpResponse

from opmanage.views.index import check_login, check_user_auth, to_page
from opmanage.forms.department import *
from opmanage.models import Department_info


# 用于判定页面访问权限的下标
check_num = 1

@check_login
@check_user_auth(check_num=check_num)
def add_department(request):
    """
        添加部门
    :param request:
    :return:
    """
    # post请求
    if request.method == "POST":
        add_departmentform = AddDepartmentForm(request.POST)
        # 字段验证通过
        if add_departmentform.is_valid():
            add_departmentform.save()
            return HttpResponse('ok')
        # 字段验证不通过
        else:
            return render(request, "opmanage/department/adddepartment.html", {'add_departmentform': add_departmentform, 'error': add_departmentform.errors})
    # 非POST请求
    else:
        add_departmentform = AddDepartmentForm()
        return render(request,"opmanage/department/adddepartment.html", {'add_departmentform': add_departmentform})


@check_login
@check_user_auth(check_num=check_num)
def del_department(request):
    """
        添加部门
    :param request:
    :return:
    """
    # post请求
    if request.method == "POST":
        del_departmentform = DelDepartmentForm(request.POST)
        # 字段验证通过
        if del_departmentform.is_valid():
            department_name = request.POST.get('department_name', None)
            # 删除数据
            Department_info.objects.filter(department_name=department_name).delete()
            return HttpResponse('ok')
        # 字段验证不通过
        else:
            return render(request, "opmanage/department/deldepartment.html", {'del_departmentform': del_departmentform, 'error': del_departmentform.errors})
    # 非POST请求
    else:
        department_name = request.GET.get('department_name')
        if department_name != None:
            del_departmentform = DelDepartmentForm({'department_name': department_name})
        else:
            del_departmentform = DelDepartmentForm()
        return render(request,"opmanage/department/deldepartment.html", {'del_departmentform': del_departmentform})



@check_login
@check_user_auth(check_num=check_num)
def updata_department(request):
    """
        更新主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        updata_departmentform = UpdataDepartmentForm(request.POST)
        # 字段验证通过
        if updata_departmentform.is_valid():
            # 添加department数据
            department_name = request.POST.get('department_name', None)

            department = Department_info.objects.get(department_name=department_name)
            updata_departmentform = UpdataDepartmentForm(request.POST, instance=department)
            updata_departmentform.save()
            # 添加department成功
            return HttpResponse('updata department %s ok' % department_name)
        # 字段验证不通过
        else:
            return render(request, "opmanage/department/updatadepartment.html", {'updata_departmentform': updata_departmentform})
    # 非POST请求
    else:
        department_name = request.GET.get('department_name')
        if department_name != None:
            department = Department_info.objects.get(department_name=department_name)
            # 参考https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#modelform
            updata_departmentform = UpdataDepartmentForm(instance=department)
        else:
            updata_departmentform = UpdataDepartmentForm()
        return render(request, "opmanage/department/updatadepartment.html", {'updata_departmentform': updata_departmentform})


@check_login
@check_user_auth(check_num=check_num)
def get_department(request):
    """
        获取主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        get_departmentform = GetDepartmentForm(request.POST)
        # 字段验证通过
        if get_departmentform.is_valid():
            department_name = request.POST.get('department_name', None)
            every_page_sum = request.POST.get('every_page_sum', 20)
            pages = request.POST.get('pages', 1)
            if department_name == '' or department_name == None:
                department_list = Department_info.objects.all()
            else:
                department_list = []
                for i in Department_info.objects.all():
                    if department_name in i.department_name:
                        department_list.append(i)
            page_department_list = to_page(department_list, pages, every_page_sum)
            # 获取相关department信息
            return render(request, "opmanage/department/getdepartment.html", {'get_departmentform': get_departmentform, 'page_department_list': page_department_list})
        # 字段验证不通过
        else:
            return render(request, "opmanage/department/getdepartment.html", {'get_departmentform': get_departmentform})
    # 非POST请求
    else:

        every_page_sum = 20
        # 获取当前页码
        pages = request.GET.get('page') or 1
        # 创建回传前端表单，如果department_name存在，返回相department_name表单，否则返回空白表单
        department_name = request.GET.get('department_name', None)
        if department_name == '' or department_name == None:
            department_list = Department_info.objects.all()
            get_departmentform = GetDepartmentForm()
        else:
            department_list = []
            for i in Department_info.objects.all():
                if department_name in i.department_name:
                    department_list.append(i)
            get_departmentform = GetDepartmentForm({'department_name': department_name})
        page_department_list = to_page(department_list, pages, every_page_sum)
        return render(request, "opmanage/department/getdepartment.html", {'get_departmentform': get_departmentform, 'page_department_list': page_department_list})



