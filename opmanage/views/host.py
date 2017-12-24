# -*- coding: utf-8 -*-
# 2017-12-04
# by why

from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.http import HttpResponse

from opmanage.forms.host import AddHostForm, DelHostForm, RenameHostForm, UpdownHostForm
from opmanage.models import Host_info
from opmanage.views.index import check_login, check_user_auth
from lib.zabbix import zabbix

# 用于判定页面访问权限的下标
check_num = 2

@check_login
@check_user_auth(check_num=check_num)
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
            host_name = request.POST.get('host_name', None)
            pro_ipaddr = request.POST.get('pro_ipaddr', None)

            # 插入数据
            # Host_info.objects.create(name=name, ipaddr=ipaddr, cloud=cloud, types=types, status=status)
            add_hostform.save()

            # 添加zabbix监控，日后添加到信号中
            add_zabbix_host(host=host_name, ip=pro_ipaddr)

            # 创建主机成功
            return HttpResponse('add,host %s ok' % host_name)

        # 字段验证不通过
        else:
            return render(request, "host/addhost.html", {'add_hostform': add_hostform, 'error': add_hostform.errors})

    # 非POST请求
    else:
        add_hostform = AddHostForm()
        return render(request, "host/addhost.html", {'add_hostform': add_hostform})


@check_login
@check_user_auth(check_num=check_num)
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

            # 删除数据
            Host_info.objects.filter(name=name).delete()

            # 删除zabbix监控
            del_zabbix_host(host=name)

            # 删除主机成功
            return HttpResponse('del host %s ok' % name)

        # 字段验证不通过
        else:
            return render(request, "host/delhost.html", {'del_hostform': del_hostform, 'error': del_hostform.errors})

    # 非POST请求
    else:
        del_hostform = DelHostForm()
        return render(request, "host/delhost.html", {'del_hostform': del_hostform})


@check_login
@check_user_auth(check_num=check_num)
def updown_host(request):
    """
        主机状态发生变化(开机关机)
    :param requets:
    :return:
    """
    # POST请求
    if request.method == "POST":
        updown_hostform = UpdownHostForm(request.POST)
        # 字段验证通过
        if updown_hostform.is_valid():
            name = request.POST.get('name', None)
            status = request.POST.get('status', None)

            # 删除数据
            Host_info.objects.filter(name=name).update(status=status)

            # 更新zabbix监控
            if status != 'running':
                disable_zabbix_host(host=name)
            else:
                enable_zabbix_host(host=name)

            # 更新主机主机成功
            return HttpResponse('change status %s to  %s ok' % (name, status))

        # 字段验证不通过
        else:
            return render(request, "host/updownhost.html",
                          {'updown_hostform': updown_hostform, 'error': updown_hostform.errors})

    # 非POST请求
    else:
        updown_hostform = UpdownHostForm()
    return render(request, "host/updownhost.html", {'updown_hostform': updown_hostform})


@check_login
@check_user_auth(check_num=check_num)
def rename_host(request):
    """
        更名主机
    :param requets:
    :return:
    """
    # POST请求
    if request.method == "POST":
        rename_hostform = RenameHostForm(request.POST)
        # 字段验证通过
        if rename_hostform.is_valid():
            name = request.POST.get('name', None)
            new_name = request.POST.get('new_name', None)

            # 删除数据
            Host_info.objects.filter(name=name).update(name=new_name)

            # 更新zabbix监控
            rename_zabbix_host(host=name, new_host=new_name)

            # 更新主机主机成功
            return HttpResponse('change host from %s to  %s ok' % (name, new_name))

        # 字段验证不通过
        else:
            return render(request, "host/renamehost.html",
                          {'rename_hostform': rename_hostform, 'error': rename_hostform.errors})

    # 非POST请求
    else:
        rename_hostform = RenameHostForm()
    return render(request, "host/renamehost.html", {'rename_hostform': rename_hostform})


def get_zabbix_template(host):
    """
        获取zabbix模板
    :return:
    """
    return '10001'


def add_zabbix_host(host, ip):
    """

    缺少主机添加模板认证

        添加主机zabbix监控
    :param requets:
    :return:
    """
    # templateid=10001

    z = zabbix()
    templateid = get_zabbix_template(host)

    print templateid

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
              "templates": [
                  {
                      "templateid": templateid
                  }
              ],
              }
    return z.getdataZabbix('host.create', params)

def del_zabbix_host(host):
    """
        删除主机zabbix监控
    :param requets:
    :return:
    """
    z = zabbix()
    id = z.hostname_to_id(host)
    params = [id, ]
    return z.getdataZabbix('host.delete', params)

def rename_zabbix_host(host, new_host):
    """
        更换被监控主机主机名
    :param host:
    :param newhost:
    :return:
    """
    z = zabbix()
    hostid = z.hostname_to_id(host)
    params = {"hostid": hostid,
              "host": new_host,
              "name": new_host}
    return z.getdataZabbix('host.update', params)


def enable_zabbix_host(host):
    """
        更换被监控主机主机名
    :param host:
    :param newhost:
    :return:
    """
    z = zabbix()
    hostid = z.hostname_to_id(host)
    params = {'hostid': hostid,
              'status': 0}
    return z.getdataZabbix('host.update', params)

def disable_zabbix_host(host):
    """
        更换被监控主机主机名
    :param host:
    :param newhost:
    :return:
    """
    z = zabbix()
    hostid = z.hostname_to_id(host)
    params = {'hostid': hostid,
              'status': 1}
    return z.getdataZabbix('host.update', params)
