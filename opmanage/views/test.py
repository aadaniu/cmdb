# -*- coding: utf-8 -*-
# 2017-11-30
# by why

from django.http import HttpResponse
from django.shortcuts import render,render_to_response,HttpResponseRedirect
from opmanage.models import User_info

def insert_data(requets):
    try:
        User_info.objects.create(name='wanghongyu',
                                 password='123456',
                                 email='wanghongyu@chuchujie.com',
                                 auth=True,
                                 jumper=True,
                                 vpn=True,
                                 phone='13552493019',
                                 department='op',
                                 ccj_admin=True,
                                 cct_admin=False)
    except:
        pass
    return HttpResponse('ok')


