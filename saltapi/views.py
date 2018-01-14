# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.shortcuts import HttpResponse,HttpResponseRedirect,render_to_response
from salt import client
from django.http import JsonResponse
import json

def exec_cmd(request):
    accect = ['cmd.run',]
    # context = accect_cmd.objects.values()
    # for i in context:
    #     accect.append(i["command"])
    if request.method == "POST":
        tgt = request.POST.get('tgt')
        tgt_type = request.POST.get('tgt_type')
        fun = request.POST.get('tgt_type')
        str_kwarg = request.POST.get('kwarg')
        if fun in accect:
            if 0:
                arg = str_kwarg
                kwarg = None
            else:
                arg = ()
                kwarg = str_kwarg
            salt_conn = client.LocalClient()
            result2 = salt_conn.cmd(tgt, fun, arg, timeout=None, tgt_type=tgt_type, ret='', jid='', full_return=False, kwarg=kwarg)
            return JsonResponse(result2, safe=False)
        else:
            data = {fun: "请检查命令是否正确或命令超权限，请联系管理员！"}
            return JsonResponse(data, safe=False)
    else:
        return render_to_response('saltapi/cmd.html')