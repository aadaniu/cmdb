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
            用户属性对应官方文档 https://www.zabbix.com/documentation/2.4/manual/api/reference/user/object#user
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
        # params = {"output": ['userid'],
        #           'filter' : {
        #                 'alias': ['wanghongyu',]
        #               }
        #           }
        # print z.getdataZabbix('user.get', params)

        # print z.userid_to_name('1')
        # print z.username_to_id('wanghongyu')

        """
        06获取模板
            template.get 对应官方文档 https://www.zabbix.com/documentation/2.4/manual/api/reference/template/get

        """
        # params = {"output": "extend"}
        # params = {"output": ['host','name', 'templateid']}
        # print z.getdataZabbix('template.get', params)

        """
        07获取报警
            alert.get 对应官方文档 https://www.zabbix.com/documentation/2.4/manual/api/reference/alert/get
        """
        # params = {"output": "extend"}
        # print z.getdataZabbix('alert.get', params)

        """
        08添加主机
            host.create 对应官方文档 https://www.zabbix.com/documentation/2.4/manual/api/reference/host/create
        """
        # params =    {"host": "agent01",
        #             "interfaces": [
        #                             {
        #                                 "type": 1,
        #                                 "main": 1,
        #                                 "useip": 1,
        #                                 "ip": "172.17.0.10",
        #                                 "dns": "",
        #                                 "port": "10050"
        #                             }
        #                         ],
        #             "groups": [
        #                         {
        #                             "groupid": "4"
        #                         }
        #                     ],
        #             }
        # print z.getdataZabbix('host.create', params)

        """
        09删除主机
            host.delete 对应官方文档 https://www.zabbix.com/documentation/2.4/manual/api/reference/host/delete
        """
        # params = ['10105',]
        # print z.getdataZabbix('host.delete', params)

        """
        10查询主机
            host.get 对应官方文档 https://www.zabbix.com/documentation/2.4/manual/api/reference/host/get
        """
        # params = {'output': 'extend',
        #           'filter': {
        #               'host': ['agent01']
        #           }}
        # 结果
        # {u'available': u'0', u'maintenance_type': u'0', u'ipmi_errors_from': u'0', u'ipmi_username': u'', u'snmp_disable_until': u'0', u'ipmi_authtype': u'0', u'ipmi_disable_until': u'0', u'lastacce
        # ss': u'0', u'snmp_error': u'', u'ipmi_privilege': u'2', u'jmx_error': u'', u'jmx_available': u'0', u'maintenanceid': u'0', u'snmp_available': u'0', u'status': u'0', u'description': u'', u'host': u'agent01', u'disable
        # _until': u'0', u'ipmi_password': u'', u'templateid': u'0', u'ipmi_available': u'0', u'maintenance_status': u'0', u'snmp_errors_from': u'0', u'ipmi_error': u'', u'proxy_hostid': u'0', u'hostid': u'10106', u'name': u'a
        # gent01', u'jmx_errors_from': u'0', u'jmx_disable_until': u'0', u'flags': u'0', u'error': u'', u'maintenance_from': u'0', u'errors_from': u'0'}

        # params = {'output': 'hostid',
        #           'filter': {
        #               'host': ['agent01']
        #           }}
        # [{u'hostid': u'10106'}]}

        # params = {'output': ['host',],
        #           'hostids': ['10106'],
        #           }
        # {u'host': u'agent01', u'hostid': u'10106'}
        # print z.getdataZabbix('host.get', params)

        #print z.hostid_to_name('10106')
        #print z.hostname_to_id('agent01')

        """
        11更新主机
            host.update 对应官方文档 https://www.zabbix.com/documentation/2.4/manual/api/reference/host/update

            需要注意的是As opposed to the Zabbix frontend, when name is the same as host, updating host will not automatically update name. Both properties need to be updated explicitly.
            翻译一下如果直接host和name相同，对于修改host是生效的。
        """





        """
        12获取报警
            alert.get 对应官方文档 https://www.zabbix.com/documentation/2.4/manual/api/reference/alert/get
        """
        # # 获取当前时间
        # import time
        # import re
        # # 当前时间
        # clock_now = time.time()
        # # 昨天时间
        # str_clock_now = str(clock_now-86400)[:-3]
        # params = {
        #     "output": "extend",
        #     # "actionids": "39",
        #     # "userids": "82",
        #     "time_from": str_clock_now,
        #     "limit": 10,
        # }
        # # print z.getdataZabbix('alert.get', params)
        # data =  z.getdataZabbix('alert.get', params)['data']
        # last_day_alert = []
        # alert = []
        # for i in data:
        #     if i[ u'message'] not in alert:
        #         alert.append(i[ u'message'])
        #         obj_re_message = re.search(r'\[([^\[\]]*)\]\[([^\[\]]*)\]\[([^\[\]]*)\]\[([^\[\]]*)\]\[([^\[\]]*)\]\[([^\[\]]*)\]\[([^\[\]]*)\]',i[u'subject'])
        #         print obj_re_message.group(1)   # action_id 我自行定义的
        #         print obj_re_message.group(2)   # 时间
        #         print obj_re_message.group(3)   # 主机名
        #         print obj_re_message.group(4)   # 报警级别
        #         print obj_re_message.group(5)   # 报警信息
        #         print re.search(r'op:(.*)',obj_re_message.group(6)).group(1)   # 运维负责人
        #         print re.search(r'server:(.*)',obj_re_message.group(7)).group(1)   # 业务负责人
        #         print i[ u'message']
        #         print i[u'clock']
        #         print i[u'subject']
        #         print i[u'eventid']
        #         last_day_alert.append({''})
        """
        13. 创建action
            action.create 对应官方文档  https://www.zabbix.com/documentation/2.4/manual/api/reference/action/create
        """

        """
        14. 修改trigger

        """
        # trigger_id = '13723'
        # z = zabbix()
        # # 0为开启，1为关闭
        # params =  {
        #             "triggerid": trigger_id,
        #             "status": '0',
        #         },
        # print z.getdataZabbix('trigger.update', params)

        """
        15. 获取历史数据
            history.get https://www.zabbix.com/documentation/2.4/manual/api/reference/history/get
            支持time_from,time_to,limit等参数
        """
        z = zabbix()
        params ={
                    "output": "extend",
                    "itemids": "24069",
                    "sortfield": "clock",
                    "sortorder": "DESC",
                    "limit": 10
                }

        print z.getdataZabbix('history.get', params)

        """
        {'status': True, 'data': [{u'itemid': u'24069', u'ns': u'889294125', u'value': u'0', u'clock': u'1515752889'},
                                  {u'itemid': u'24069', u'ns': u'882639616', u'value': u'0', u'clock': u'1515752859'},
                                  {u'itemid': u'24069', u'ns': u'871681861', u'value': u'0', u'clock': u'1515752829'},
                                  {u'itemid': u'24069', u'ns': u'866340256', u'value': u'0', u'clock': u'1515752799'},
                                  {u'itemid': u'24069', u'ns': u855850482', u'value': u'0', u'clock': u'1515752769'},
                                  {u'itemid':u'24069',u'ns': u'849023277', u'value': u'0', u'clock': u'1515752739'},
                                  {u'itemid': u'24069', u'ns': u'838169491', u'value': u'0', u'clock': u'1515752709'},
                                  {u'itemid': u'24069', u'ns': u'832910980', u'value': u'0', u'clock': u'1515752679'},
                                  {u'itemid': u'24069', u'ns': u'822549749', u'value': u'0', u'clock': u'1515752649'},
                                  {u'itemid': u'24069', u'ns': u'817882180', u'value': u'0', u'clock': u'1515752619'}]}
        """

        """
        16. 获取主机iterm
            item.get https://www.zabbix.com/documentation/2.4/manual/api/reference/item/get
        """

        # z = zabbix()
        # host_id = z.hostname_to_id('Zabbix server')
        #
        # params ={
        #             "output": ["itemids", "key_"],
        #             "hostids": host_id,
        #             "search": {
        #                           "key_": "why"
        #                       },
        #             "sortfield": "name"
        #         }
        # # print z.getdataZabbix('item.get', params)['data'][0]['key_']
        # print z.getdataZabbix('item.get', params)['data'][0]['itemid']


        # import json
        # return HttpResponse(json.dumps(z.getdataZabbix('item.get', params)))

        """41项
        Action  报警动作的增删改查   对于cmdb用不到，我们更希望手动来创建
        Alert   报警信息查询  对于cmdb可以用来生成运维报表
        API info    获取api版本
        Application
        Configuration   配置导入导出
        Discovered host
        Discovered service
        Discovery check
        Discovery rule
        Event
        Graph
        Graph item
        Graph prototype
        History 获取报警历史记录
        Host    主机的增删改查，添加移除主机组
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
        Template 包括模板的增删改查，模板添加移除到模板组 对于cmdb来说可以用
        Template screen 模板视图的操作，我们也没用到这个
        Template screen item 同上，没有用过
        Trigger
        Trigger prototype
        User 包含用户创建的增删改查，用户报警方式的增删改查，以及部分用户权限查询 对于cmdb来说可以用
        User group 包含用户组的增删改查，以及部分用户组权限查 对于cmdb来说可以用
        User macro 全局变量和局部变量的增删改查  对于cmdb可能会用到
        Web scenario 说实话我没找到这个
        """


    except Exception as e:
        return HttpResponse(e)
    return HttpResponse('ok')