# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.shortcuts import HttpResponse,HttpResponseRedirect,render_to_response
from salt import client
from django.http import JsonResponse
import json

def exec_cmd(request):
    """
        用于web端批量salt
    :param request:
    :return:
    """
    # 允许命令列表
    accect = ['cmd.run',]
    # context = accect_cmd.objects.values()
    # for i in context:
    #     accect.append(i["command"])
    if request.method == "POST":
        tgt = request.POST.get('tgt')
        tgt_type = request.POST.get('tgt_type[]')
        """
        glob - Bash命令方式(默认)
        pcre(E) - 正则匹配规则
        list(L) - 主机列表规则
        grain(G) - Grain匹配规则
        grain_pcre(P) - Grain正则匹配规则
        pillar(I) - Pillar匹配规则
        pillar_pcre - Pillar正则匹配规则
        nodegroup(N) - 主机组规则
        range(R) - 服务器范围匹配
        compound(C) - 条件匹配
        ipcidr(S) - IP或网段匹配规则
        英文参考 https://docs.saltstack.com/en/latest/ref/clients/
        glob - Bash glob completion - Default
        pcre - Perl style regular expression
        list - Python list of hosts
        grain - Match based on a grain comparison
        grain_pcre - Grain comparison with a regex
        pillar - Pillar data comparison
        pillar_pcre - Pillar data comparison with a regex
        nodegroup - Match on nodegroup
        range - Use a Range server for matching
        compound - Pass a compound match string
        ipcidr - Match based on Subnet (CIDR notation) or IPv4 address.
        """
        fun = request.POST.get('fun')
        str_kwarg = request.POST.get('kwarg')
        if fun in accect:
            salt_conn = client.LocalClient()
            result2 = salt_conn.cmd(tgt, fun, arg=[str_kwarg,], timeout=None, expr_form=tgt_type, ret='', jid='', full_return=False, kwarg=None)
            # 写入历史数据
            #
            return JsonResponse(result2, safe=False)
        else:
            data = {fun: "请检查命令是否正确或命令超权限，请联系管理员！"}
            return JsonResponse(data, safe=False)
    else:
        return render_to_response('saltapi/cmd.html')



def hostpaller(request):
    """
        salt paller管理
            salt主机组nodegroup不支持动态，可以通过python动态修改配置文件，salt获取主机组也是salt-master获取配置文件原理实现；
            salt的paller支持动态获取资源，由cmdb提供api，对应salt端脚本即可，并且可以为fabric提供获取主机组的接口，一举两得。
        # http://blog.51cto.com/lihuipeng/1789433
    :param request:
    :return:
    """
    pass


def crontab_plan(request):
    """
        通过salt添加定时任务
    :param request:
    :return:
    """
    pass


def custom_module(request):
    """
        用于自定义模块进行组合
    :param request:
    :return:
    """
    pass




