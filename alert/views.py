# -*- coding: utf-8 -*-
# 2018-01-03
# by why

from __future__ import unicode_literals

# Create your views here.

from django.shortcuts import render,render_to_response,HttpResponseRedirect,redirect
from django.http import HttpResponse
import time
import re

from opmanage.views.index import check_login, check_user_auth, to_page
from alert.forms import *
from alert.models import *
from lib.zabbix import zabbix

check_num = 2

@check_login
@check_user_auth(check_num=check_num)
def get_historyalert(request):
    """
        获取报警
    :param request:
    :return:u
    """
    # POST请求
    if request.method == "POST":
        get_historyalertform = GetHistoryAlertForm(request.POST)
        # 字段验证通过
        if get_historyalertform.is_valid():
            search_word = request.POST.get('search_word', None)
            every_page_sum = request.POST.get('every_page_sum', 20)
            pages = request.POST.get('pages', 1)
            if search_word == '' or search_word == None:
                historyalert_list = HistoryAlert_info.objects.all().order_by('-clock')
            else:
                historyalert_list = []
                for i in HistoryAlert_info.objects.all().order_by('-clock'):
                    if search_word in i.subject:
                        historyalert_list.append(i)
            page_historyalert_list = to_page(historyalert_list, pages, every_page_sum)
            # 获取相关alert信息
            return render(request, "alert/gethistoryalert.html", {'get_historyalertform': get_historyalertform, 'page_historyalert_list': page_historyalert_list})
        # 字段验证不通过
        else:
            return render(request, "alert/gethistoryalert.html", {'get_historyalertform': get_historyalertform})
    # 非POST请求
    else:
        every_page_sum = 20
        # 获取当前页码
        pages = request.GET.get('page') or 1
        # 创建回传前端表单，如果搜索词存在，返回搜索词表单，否则返回空白表单
        search_word = request.GET.get('search_word', None)
        if search_word == '' or search_word == None:
            historyalert_list = HistoryAlert_info.objects.all().order_by('-clock')
            get_historyalertform = GetHistoryAlertForm()
        else:
            historyalert_list = []
            for i in HistoryAlert_info.objects.all().order_by('-clock'):
                if search_word in i.subject:
                    historyalert_list.append(i)
            get_historyalertform = GetHistoryAlertForm({'search_word': search_word})
        page_historyalert_list = to_page(historyalert_list, pages, every_page_sum)
        return render(request, "alert/gethistoryalert.html", {'get_historyalertform': get_historyalertform, 'page_historyalert_list': page_historyalert_list})


@check_login
@check_user_auth(check_num=check_num)
def get_last_10_alert(request):
    alert_list = HistoryAlert_info.objects.all().order_by('-clock')[0:9]
    return render(request, "alert/getsomealert.html", {'alert_list': alert_list})


@check_login
@check_user_auth(check_num=check_num)
def get_last_day_alert(request):
    # 当前时间
    clock_now = time.time()
    # 昨天时间
    clock_lastday = clock_now - 86400
    alert_list = HistoryAlert_info.objects.filter(clock__gte=clock_lastday).order_by('-clock')
    return render(request, "alert/getsomealert.html", {'alert_list': alert_list})


@check_login
@check_user_auth(check_num=check_num)
def get_closed_alert(request):
    alert_list = HistoryAlert_info.objects.filter(trigger_status='closed').order_by('-clock')
    return render(request, "alert/getsomealert.html", {'alert_list': alert_list})


@check_login
@check_user_auth(check_num=check_num)
def edit_alert(request):
    """
        编辑报警处理结果
    :param request:
    :return:
    """
    # POST请求
    if request.method == "POST":
        edit_alertform = EditHistoryAlertForm(request.POST)
        # 字段验证通过
        if edit_alertform.is_valid():
            # 添加处理结果数据
            edit_alertform.save()
            # 添加domain成功
            return HttpResponse('edit_alert')
        # 字段验证不通过
        else:
            return render(request, "alert/editalert.html", {'edit_alertform': edit_alertform})
    # 非POST请求
    else:
        event_id = request.GET.get('event_id')
        if event_id != None:
            alert = HistoryAlert_info.objects.get(event_id=event_id)
            edit_alertform = EditHistoryAlertForm(instance=alert)
        else:
            edit_alertform = EditHistoryAlertForm()
        return render(request, "alert/editalert.html", {'edit_alertform': edit_alertform})

def add_alert(request):
    """
       用于zabbix直接添加alert接口
    :param request:
    :return:
    """
    if request.method == 'POST':
        request_ipaddr = request.META.get("REMOTE_ADDR",None)
        print request_ipaddr
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        # obj_re_subject = re.search(r'\[([^\[\]]*)\]\[([^\[\]]*)\]\[([^\[\]]*)\]\[([^\[\]]*)\]\[([^\[\]]*)\]\[([^\[\]]*)\]\[([^\[\]]*)\]',subject)
        obj_re_message = re.search(r'(\d+)*:(\d+)*', message)
        # print obj_re_subject.group(1)   # action_id 我自行定义的
        # print obj_re_subject.group(2)   # 时间
        # print obj_re_subject.group(3)   # 主机名
        # print obj_re_subject.group(4)   # 报警级别
        # print obj_re_subject.group(5)   # 报警信息
        # print re.search(r'op:(.*)',obj_re_subject.group(6)).group(1)   # 运维负责人
        # print re.search(r'server:(.*)',obj_re_subject.group(7)).group(1)   # 业务负责人
        # print obj_re_message.group(1)   # trigger_id
        # print obj_re_message.group(2)   # event_id
        HistoryAlert_info.objects.create(clock=123123,# clock=time.time(),
                                         subject=subject,
                                         event_id=obj_re_message.group(2),
                                         trigger_id=obj_re_message.group(1),
                                         trigger_status='open',
                                         cause= None,
                                         solution= None,
                                         alert_status= '')
        return HttpResponse('ok')
    else:
        return render(request,'alert/addalert.html')


# if 'cpu' in subject:
#     # 获取cpu使用率最高的几个进程	ps aux | sort -k3nr | head -4
# 	# 获取主机LB的请求数
# 	# 自动处理 获取主机类型，决定reload那些程序
#
# if 'memory' in subject:
# 	# 获取内存使用率最高的几个进程	ps aux | sort -k4nr | head -3
# 	# sar -B 1 3
# 	# cat /proc/meminfo		| grep Slab	        	sudo sysctl -w vm.drop_caches=3
# 	# 自动处理 获取主机类型，决定reload那些程序
# if 'time_wait' in subject:
# 	# 获取快速回收参数	grep tcp_tw_recycle /etc/sysctl.conf
# 	# 获取time_wait		netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'
# 	#
# if 'network outcoming' in subject:
# 	# 获取占用网卡
# 	yum install libpcap nethogs
#
# 	dstat -nf
# 	sar -n DEV 1 4
# 	nethogs	可以看进程nethogs -c 10 -t




# 	[root@why 01:05:10 ~]#vmstat
# procs -----------memory---------- ---swap-- -----io---- --system-- -----cpu-----
#  r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
#  1 40      0  70416    208  35820    0    0    29    28    1    3  1  1 97  0  0
# if 'iowait'
# 	# 获取占用写入磁盘
# 	pidstat -d 1
# if 'FreeSpace'
# 	# 获取占用磁盘空间大的目录
# if 'Zabbix agent'
# 	# 获取zabbix运行情况
# 	# 获取主机运行情况

# elb

# if '4xx'
#     # 获取4xx日志，前提日志格式统一
# 	# 获取发版情况
# if '5xx'
# 	# 获取5xx日志
# 	# 获取发版情况
# if 'Latency'
# 	# 获取当前请求数
# 	# 获取发版情况
# 	# 获取后端超过阈值的日志
# if 'UnHealthyHostCount'
# 	# 获取挂掉主机
# 	# 检测主机是否能ssh
# 	# 检测主机上服务

# mysql
#
#
# redis
#
#
# memcache
#
#
# JVM
#
#
#
#
# 单独服务监控
# zabbix
# cmdb
# kafka
# es
# 等等
#
#
# 业务监控



@check_login
@check_user_auth(check_num=check_num)
def close_trigger(request):
    """
        更改trigger
    :param request:
    :return:
    """
    event_id = request.POST.get('event_id')
    trigger_id = request.POST.get('trigger_id')
    # ClosedTrigger_info.objects.create()
    z = zabbix()
    # 0为开启，1为关闭
    params =  {
                "triggerid": trigger_id,
                "status": '1',
            },
    HistoryAlert_info.objects.filter(event_id=event_id).updata(trigger_status='closed')
    z.getdataZabbix('trigger.update', params)
    # {'status': True, 'data': {u'triggerids': [u'13723']}}
