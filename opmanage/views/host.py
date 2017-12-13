# -*- coding: utf-8 -*-
# 2017-12-04
# by why

from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.http import HttpResponse

from lib.zabbix import zabbix
from opmanage.forms import AddHostForm,DelHostForm
from opmanage.models import Host_info


"""
id name IP 机型 实例状态 标签信息
"""

def add_host(request):
    """
        添加主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        add_hostform = AddHostForm(request.POST)
        # 字段验证通过
        if add_hostform.is_valid():
            name = request.POST.get('name', None)
            ipaddr = request.POST.get('ipaddr', None)
            cloud = request.POST.get('ipaddr', None)
            types = request.POST.get('ipaddr', None)
            status = request.POST.get('ipaddr', None)

            # 插入数据
            Host_info.objects.create(name=name, ipaddr=ipaddr, cloud=cloud, types=types, status=status)

            # 添加zabbix监控
            add_zabbix(host=name, ip=ipaddr)

            # 创建用户成功
            return HttpResponse('add,host %s ok' % name)

        # 字段验证不通过
        else:
            return render(request, "addhost.html", {'add_hostform': add_hostform, 'error': add_hostform.errors})

    # 非POST请求
    else:
        add_hostform = AddHostForm()
        return render(request, "addhost.html", {'add_hostform': add_hostform})

def del_host(request):
    """
        删除主机
    :param requets:
    :return:
    """
    # POST请求
    if request.method == "POST":
        del_hostform = DelHostForm(request.POST)
        # 字段验证通过
        if del_hostform.is_valid():
            name = request.POST.get('name', None)

            # 插入数据
            Host_info.objects.delete(name=name)

            # 添加zabbix监控
            del_zabbix(host=name)

            # 创建用户成功
            return HttpResponse('del host %s ok' % name)

        # 字段验证不通过
        else:
            return render(request, "delhost.html", {'del_hostform': del_hostform, 'error': del_hostform.errors})

    # 非POST请求
    else:
        del_hostform = DelHostForm()
        return render(request, "delhost.html", {'del_hostform': del_hostform})


def get_zabbix_template():
    """
        获取zabbix模板
    :return:
    """
    pass


def add_zabbix(requets, host, ip):
    """

    缺少主机添加模板认证

        添加主机zabbix监控
    :param requets:
    :return:
    """

    z = zabbix()

    params = {"host": host,
              "interfaces": [
                  {
                      "type": 1,
                      "main": 1,
                      "useip": 1,
                      "ip": ip,
                      "dns": "",
                      "port": "10050"
                  }
              ],
              "groups": [
                  {
                      "groupid": "4"
                  }
              ],
              }
    return z.getdataZabbix('host.create', params)

def del_zabbix(requets, host):
    """
        删除主机zabbix监控
    :param requets:
    :return:
    """
    z = zabbix()
    id = z.hostname_to_id(host)
    params = [id, ]
    return z.getdataZabbix('host.delete', params)

def check_op_auth(auth):
    """
        检查运维权限
    :param auth:
    :return:
    """
    if auth == 1:
        return True
    else:
        return False


