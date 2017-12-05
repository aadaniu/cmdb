# -*- coding: utf-8 -*-
# 2017-11-30
# by why

from django.http import HttpResponse
from django.shortcuts import render,render_to_response,HttpResponseRedirect
from opmanage.models import User_info

def insert_data(requets):
    """
        添加测试数据
    :param requets:
    :return:
    """
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

from lib.sendmail import sendmail_table, sendmail_general

def sendtable(requets):
    """
        测试发送表格邮件
    :param requets:
    :return:
    """
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


    try:
        sendmail_table(subject, temail, dataDict, user)
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse('ok')


def send(request):
    """
        测试发送简单邮件
    :param request:
    :return:
    """
    # try:
    #     sendmail_general('hello world','why@whysdomain.com')
    # except Exception as e:
    #     return HttpResponse(e)
    # return HttpResponse('ok')
    sendmail_general('Test','helloworld',['why@whysdomain.com',])
    return HttpResponse('ok')


from lib.zabbix import zabbix


def test_zabbix(request):
    """
        测试zabbix功能
    :param request:
    :return:
    """
    try:
        z = zabbix()
        # print z.getallhost()
        # print z.usergroup_create('test02',['1','2'])
    except Exception as e:
        return HttpResponse(e)
    return HttpResponse('ok')






