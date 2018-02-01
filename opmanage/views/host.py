# -*- coding: utf-8 -*-
# 2017-12-04
# by why

from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.http import HttpResponse

from opmanage.forms.host import *
from opmanage.models import Host_info
from opmanage.views.index import check_login, check_user_auth, to_page
from workorder.models import Host_WorkOrder_info, Status_WorkOrder_info
from workorder.views import step_status_ok
from lib.zabbix import zabbix

# 用于判定页面访问权限的下标
check_num = 2

@check_login
@check_user_auth(check_num=check_num)
def add_host(request, notice=None, show=None):
    """
        添加主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        form = AddHostForm(request.POST)
        # 字段验证通过
        if form.is_valid():
            cloud_type = request.POST.get('cloud_type')
            host_type = request.POST.get('host_type')
            host_number = request.POST.get('host_number')
            disk = request.POST.get('disk')
            pubipaddr = request.POST.get('pro_ipaddr')
            serverline = request.POST.get('serverline')
            host_workorder_id = request.POST.get('host_workorder_id')
            step_num = request.POST.get('step_num')

            # 创建主机
            create_host(cloud_type,host_type,host_number,disk,pubipaddr,serverline)

            # 更新workorder
            func_status = step_status_ok(host_workorder_id, step_num)

            if func_status:
                # 创建主机成功
                return HttpResponse('add host ok')
            else:
                return HttpResponse('add host false')

        # 字段验证不通过
        else:
            return render(request, "opmanage/host/addhost.html", {'form': form, 'notice': notice, 'show': show})

    # 非POST请求
    else:
        host_workorder_id = request.GET.get('host_workorder_id', None)
        step_num = request.GET.get('step_num', None)
        if host_workorder_id != None:
            host_workorder_obj = Host_WorkOrder_info.objects.filter(host_workorder_id=host_workorder_id).first()
            form = AddHostForm(initial={'step_num': step_num,
                                        'cloud_type': host_workorder_obj.cloud_type,
                                        'host_type': host_workorder_obj.host_type,
                                        'host_number': host_workorder_obj.host_number,
                                        'disk': host_workorder_obj.disk,
                                        'pubipaddr': host_workorder_obj.pubipaddr,
                                        'serverline': host_workorder_obj.serverline_name,
                                        'host_workorder_id': host_workorder_id,
                                        })
        else:
            form = AddHostForm()
        return render(request, "opmanage/host/addhost.html", {'form': form, 'notice': notice, 'show': show})


@check_login
@check_user_auth(check_num=check_num)
def del_host(request, notice=None, show=None):
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
            host_name = request.POST.get('host_name', None)

            # 删除数据
            Host_info.objects.filter(host_name=host_name).delete()

            # 删除zabbix监控
            del_zabbix_host(host=host_name)

            # 删除主机成功
            return HttpResponse('del host %s ok' % host_name)

        # 字段验证不通过
        else:
            return render(request, "opmanage/host/delhost.html", {'del_hostform': del_hostform, 'error': del_hostform.errors})

    # 非POST请求
    else:
        host_name = request.GET.get('host_name')
        if host_name != None:
            del_hostform = DelHostForm({'host_name': host_name})
        else:
            del_hostform = DelHostForm()
        return render(request, "opmanage/host/delhost.html", {'del_hostform': del_hostform})

@check_login
@check_user_auth(check_num=check_num)
def updata_host(request, notice=None, show=None):
    """
        更新主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        updata_hostform = UpdataHostForm(request.POST)
        # 字段验证通过
        if updata_hostform.is_valid():
            # 添加host数据
            host_name = request.POST.get('host_name', None)
            host = Host_info.objects.get(host_name=host_name)
            updata_hostform = UpdataHostForm(request.POST, instance=host)
            updata_hostform.save()
            # 添加host成功
            return HttpResponse('updata host %s ok' % host_name)
        # 字段验证不通过
        else:
            return render(request, "opmanage/host/updatahost.html", {'updata_hostform': updata_hostform})
    # 非POST请求
    else:
        host_name = request.GET.get('host_name')
        if host_name != None:
            host = Host_info.objects.get(host_name=host_name)
            # 参考https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#modelform
            updata_hostform = UpdataHostForm(instance=host)
        else:
            updata_hostform = UpdataHostForm()
        return render(request, "opmanage/host/updatahost.html", {'updata_hostform': updata_hostform})


@check_login
@check_user_auth(check_num=check_num)
def get_host(request, notice=None, show=None):
    """
        获取主机
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        get_hostform = GetHostForm(request.POST)
        # 字段验证通过
        if get_hostform.is_valid():
            host_name = request.POST.get('host_name', None)
            every_page_sum = request.POST.get('every_page_sum', 20)
            pages = request.POST.get('pages', 1)
            if host_name == '' or host_name == None:
                host_list = Host_info.objects.all()
            else:
                host_list = []
                for i in Host_info.objects.all():
                    if host_name in i.host_name:
                        host_list.append(i)
            page_host_list = to_page(host_list, pages, every_page_sum)
            # 获取相关host信息
            return render(request, "opmanage/host/gethost.html", {'get_hostform': get_hostform, 'page_host_list': page_host_list})
        # 字段验证不通过
        else:
            return render(request, "opmanage/host/gethost.html", {'get_hostform': get_hostform})
    # 非POST请求
    else:
        every_page_sum = 20
        # 获取当前页码
        pages = request.GET.get('page') or 1
        # 创建回传前端表单，如果host_name存在，返回相host_name表单，否则返回空白表单
        host_name = request.GET.get('host_name', None)
        if host_name == '' or host_name == None:
            host_list = Host_info.objects.all()
            get_hostform = GetHostForm()
        else:
            host_list = []
            for i in Host_info.objects.all():
                if host_name in i.host_name:
                    host_list.append(i)
            get_hostform = GetHostForm({'host_name': host_name})
        page_host_list = to_page(host_list, pages, every_page_sum)
        return render(request, "opmanage/host/gethost.html", {'get_hostform': get_hostform, 'page_host_list': page_host_list})



@check_login
@check_user_auth(check_num=check_num)
def updown_host(request, notice=None, show=None):
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
            host_name = request.POST.get('host_name', None)
            status = request.POST.get('status', None)

            # 删除数据
            Host_info.objects.filter(host_name=host_name).update(status=status)

            # 更新zabbix监控
            if status != 'running':
                disable_zabbix_host(host=host_name)
            else:
                enable_zabbix_host(host=host_name)

            # 更新主机主机成功
            return HttpResponse('change status %s to  %s ok' % (host_name, status))

        # 字段验证不通过
        else:
            return render(request, "opmanage/host/updownhost.html",
                          {'updown_hostform': updown_hostform, 'error': updown_hostform.errors})

    # 非POST请求
    else:
        updown_hostform = UpdownHostForm()
    return render(request, "host/updownhost.html", {'updown_hostform': updown_hostform})


@check_login
@check_user_auth(check_num=check_num)
def rename_host(request, notice=None, show=None):
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
            host_name = request.POST.get('host_name', None)
            new_name = request.POST.get('new_name', None)

            # 删除数据
            Host_info.objects.filter(host_name=host_name).update(name=new_name)

            # 更新zabbix监控
            rename_zabbix_host(host=host_name, new_host=new_name)

            # 更新主机主机成功
            return HttpResponse('change host from %s to  %s ok' % (host_name, new_name))

        # 字段验证不通过
        else:
            return render(request, "opmanage/host/renamehost.html",
                          {'rename_hostform': rename_hostform, 'error': rename_hostform.errors})

    # 非POST请求
    else:
        rename_hostform = RenameHostForm()
    return render(request, "opmanage/host/renamehost.html", {'rename_hostform': rename_hostform})


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
    try:
        z = zabbix()
        id = z.hostname_to_id(host)
        params = [id, ]
        return z.getdataZabbix('host.delete', params)
    except:
        pass

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


def create_host(cloud_type,host_type,host_number,disk,pubipaddr,serverline):
    """
        通过api创建主机
    :param cloud_type:
    :param host_type:
    :param host_number:
    :param disk:
    :param pubipaddr:
    :param serverline:
    :return:
    """
    pass
