# -*- coding: utf-8 -*-
# 2017-11-30
# by why

from django.http import HttpResponse
from django.shortcuts import render,render_to_response,HttpResponseRedirect


from opmanage.models import User_info,Host_info,Department_info,Serverline_info,Lb_info
from lib.jenkinsapi import getLastThreeBuildTimes



def test(request):
    return render(request,"test.html")

def test_cmdbbase(request):
    return render(request,"cmdbbase.html")

def testjenkins(request):
    return HttpResponse(getLastThreeBuildTimes('api-cart-master-deploy'))


def insert_host(requets):
    """
        添加测试数据
    :param requets:
    :return:
    """
    try:

        Host_info.objects.create()
    except Exception as e:
        return HttpResponse(e)


def insert_data(requets):
    """
        添加测试数据
    :param requets:
    :return:
    """
    try:
        # Department_info.objects.create(department_name='op',department_leader='guosong',department_email='op@chuchujie.com')
        # Department_info.objects.create(department_name='shop',department_leader='lishun',department_email='shop@chuchujie.com')
        # Department_info.objects.create(department_name='ads',department_leader='yinzhiwei',department_email='ads@chuchujie.com')
        # Department_info.objects.create(department_name='test',department_leader='mayanqin',department_email='test@chuchujie.com')
        # Department_info.objects.create(department_name='data',department_leader='wangyujie',department_email='data@chuchujie.com')
        # Department_info.objects.create(department_name='client',department_leader='wangjing',department_email='client@chuchujie.com')
        # Department_info.objects.create(department_name='java',department_leader='guming',department_email='java@chuchujie.com')
        # Serverline_info.objects.create(serverline_name='shop-api-order',serverline_leader='jijian',serverline_op_leader='wanghongyu',department_id='2')
        # Serverline_info.objects.create(serverline_name='dwxk-api-cart',serverline_leader='jianpanlong',serverline_op_leader='huangqingwu',department_id='2')
        # User_info.objects.create(username='wanghongyu',password='123456',email='wanghongyu@whysdomain.com',auth='1',jumper='1',vpn='1',
        #                          phone='13552493019', department_id = 1, git= '1',zabbix='1',jenkins='1')
        i = 0
        while i < 301:
            i = i + 1
            # print i
            lb_name = 'test%s' % i
            Lb_info.objects.create(lb_name=lb_name,cname='0000@whysdomain.com', ipaddr= '22.2.2.2', role_from_port= '80', role_to_port= '3306', cloud= 'aws', types= 'internet-facing', serverline_id=1)
        return HttpResponse('ok')
    except Exception as e:
        return HttpResponse(e)


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



import logging, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger('default')

def log_test(request):
    logger.error("level error test")
    logger.info("level info test")
    logger.warning("level info warning")

    return HttpResponse('ok')







