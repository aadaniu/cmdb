# -*- coding: utf-8 -*-
# 2017-11-30
# by why

from django.http import HttpResponse
from django.shortcuts import render,render_to_response,HttpResponseRedirect
from opmanage.models import User_info

def insert_data(requets):
    try:
        User_info.objects.create(username='wanghongyu',
                                 password='123456',
                                 email='wanghongyu@whysdomain.com',
                                 auth=True,
                                 jumper=True,
                                 vpn=True,
                                 phone='13552493019',
                                 department='op',
                                 zabbix=True,
                                 kibana=False)
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse('ok')

from lib.sendmail import sendmail_table

def sendtable(requets):
    subject = '磁盘使用情况'
    temail = ['why@whysdomain.com',]
    # 原来的sendmail，不支持不同的表头
    # columns = ['主机名', '磁盘', '磁盘使用率']
    # data1 = [['why01','/','88%'],['why02','/','85%']]
    # count = len(data1)
    # table_name1 = '磁盘使用率大于%d%%的主机磁盘，共计%s例' % (80,count)
    # dataDict = {}
    # dataDict[table_name1] =data1
    # data2 = [['why01','/','1%'],['why02','/','2%']]
    # count = len(data2)
    # table_name2 = '磁盘使用率小于%d%%的主机磁盘，共计%s例' % (20,count)
    # dataDict[table_name2] =data2
    dataDict = []
    data1 = {}
    data1['columns'] = ['主机名', '磁盘', '磁盘最小使用率']
    data1['data'] = [['why01','/','88%'],['why02','/','85%']]
    data1['title'] = '磁盘使用率大于%d%%的主机磁盘，共计%s例' % (80,len(data1['data']))
    dataDict.append(data1)
    data2 = {}
    data2['columns'] = ['主机名', '磁盘', '磁盘最大使用率']
    data2['data'] = [['why03','/','1%'],['why04','/','2%']]
    data2['title'] = '磁盘使用率小于%d%%的主机磁盘，共计%s例' % (20,len(data2['data']))
    dataDict.append(data2)
    user = '王宏宇'
    print dataDict

    try:
        sendmail_table(subject, temail, dataDict, user)
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse('ok')


