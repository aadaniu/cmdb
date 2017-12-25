# -*- coding: utf-8 -*-
# 2017-12-24
# by why

import time
import json
from django.shortcuts import render,render_to_response,HttpResponseRedirect,redirect
from django.http import HttpResponse

from opmanage.views.index import check_login, check_user_auth
from opmanage.forms.department import AddDepartmentForm, DelDepartmentForm
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
            # department_name = request.POST.get('department_name', None)
            # department_leader = request.POST.get('department_leader', None)
            # department_email = request.POST.get('department_email', None)
            # # 插入数据
            # Department_info.objects.create(department_name=department_name,department_leader=department_leader,department_email=department_email)
            add_departmentform.save()
            return HttpResponse('ok')
        # 字段验证不通过
        else:
            return render(request, "department/adddepartment.html", {'add_departmentform': add_departmentform, 'error': add_departmentform.errors})
    # 非POST请求
    else:
        add_departmentform = AddDepartmentForm()
        return render(request,"department/adddepartment.html", {'add_departmentform': add_departmentform})


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
            return render(request, "department/deldepartment.html", {'del_departmentform': del_departmentform, 'error': del_departmentform.errors})
    # 非POST请求
    else:
        del_departmentform = DelDepartmentForm()
        return render(request,"department/deldepartment.html", {'del_departmentform': del_departmentform})
