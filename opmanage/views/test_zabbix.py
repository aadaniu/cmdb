# -*- coding: utf-8 -*-
# 2017-12-06
# by why

from django.http import HttpResponse
from django.shortcuts import render,render_to_response,HttpResponseRedirect


from lib.zabbix import zabbix


def test_zabbix(request):
    """
        测试zabbix功能
        本方法用于测试CMDB的zabbix模块，并作为zabbix模块的文档
    :param request:
    :return:
    """
    try:
        z = zabbix()
        # print z.getallhost()
        # print z.usergroup_create('test01',['1','2'])
        # print z.usergroup_delete(['13','16'])


        """
        01添加用户组
            usergroup.create 对应官方文档 https://www.zabbix.com/documentation/2.4/manual/api/reference/usergroup/create
            文档介绍可以定义rights，可限制组内用户访问主机组。日后有主机组会进行测试？
            示例返回值
            {'status': True, 'data': {u'usrgrpids': [u'20']}}
        """
        # params = {"name": 'test01'}   # 为必须
        # params["userids"] = ['1','2'] # 组内用户
        # print z.getdataZabbix('usergroup.create',params)

        """
        02删除用户组
            usergroup.delete 对应官方文档 https://www.zabbix.com/documentation/2.4/manual/api/reference/usergroup/delete
            示例返回值
            {'status': True, 'data': {u'usrgrpids': [u'20']}}
        """
        # params = ['20',]
        # print z.getdataZabbix('usergroup.delete', params)

        """
        03添加用户
            user.create 对应官方文档 https://www.zabbix.com/documentation/2.4/manual/api/reference/user/create
            示例返回值
            {'status': True, 'data': {u'userids': [u'3']}}
        """
        # params = {'alias': 'test03',
        #           'passwd': '123456'}
        # params['name'] = '03'
        # params['surname'] = 'test'
        # params['usrgrps'] = [{'usrgrpid': '7'}]   # 一个用户可以在多个组内
        # params['user_medias'] = [   # 这里为什么是个列表，因为可以不同的时段对应不同的报警媒介
        #                               {'mediatypeid': '1',
        #                                'sendto': 'test@whysdomain.com',
        #                                'active': '0',      # 0为开启
        #                                'severity': '63',   # 对应1111 1111 各个报警级别
        #                                'period': '1-7,00:00-24:00'
        #                               }
        #                         ]
        # print z.getdataZabbix('user.create', params)

        """
        04删除用户
            user.delete 对应官方文档 https://www.zabbix.com/documentation/2.4/manual/api/reference/user/delete
            示例返回值
            {'status': True, 'data': {u'userids': [u'5', u'6']}}
        """
        # params = ['5','6']
        # print z.getdataZabbix('user.delete', params)

        """
        05获取用户
            user.get 对应官方文档 https://www.zabbix.com/documentation/2.4/manual/api/reference/user/get
            文档中可供查询的参数有mediaids，mediatypeids，usrgrpids和userids
        """
        # params = {"output": "extend"}   # 获取所有用户
        # params = {"output": ['name','id']}    # 获取所有用户的指定条件
        # params = {"output":['alias','userid'],'userids': '1'} # 获取指定id的用户的指定信息
        # print z.getdataZabbix('user.get', params)



        """41项
        Action  报警动作的增删改查
        Alert   报警信息查询
        API info    获取api版本
        Application
        Configuration
        Discovered host
        Discovered service
        Discovery check
        Discovery rule
        Event
        Graph
        Graph item
        Graph prototype
        History
        Host
        Host group
        Host interface
        Host prototype
        Icon map
        Image
        Item
        Item prototype
        IT service
        LLD rule
        Maintenance
        Map
        Media
        Media type
        Proxy
        Screen
        Screen item
        Script
        Template
        Template screen
        Template screen item
        Trigger
        Trigger prototype
        User 包含用户创建的增删改查，用户报警方式的增删改查，以及部分用户权限查询
        User group 包含用户组的增删改查，以及部分用户组权限查
        User macro 全局变量和局部变量的增删改查
        Web scenario 说实话我没找到这个
        """

    except Exception as e:
        return HttpResponse(e)
    return HttpResponse('ok')