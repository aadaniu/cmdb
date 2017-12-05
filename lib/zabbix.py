# -*- coding: utf-8 -*-
# 2017-12-05
# by why

import httplib
import json
import traceback
from datetime import datetime, timedelta, date

from lib.load_config import zabbix_api_username,zabbix_api_password,zabbix_api_host,zabbix_api_url


class zabbix():
    """
    zabbix根据zabbix官方文档
        https://www.zabbix.com/documentation/2.4/manual/api/reference
    构建

    包括基本的
        __init__，加载Token
        _getToken，获取Token
        _queryZabbix,通过self.Token进行请求
        其他方法根据官方文档，通过_queryZabbix方法进行请求
        api和方法对应示例
            API: user.addmedia 对应 Function: user_addmedia
    """
    def __init__(self):
        """
            构造函数，获取Token
        :return:
        """
        self.token = None
        self._getToken()

    def _queryZabbix(self, data=None, retry = 3):
        """
            构造API请求
        :param data: 请求数据
        :param retry: 重试次数
        :return:
        """
        HOST = zabbix_api_host
        URL = zabbix_api_url
        HEADER = {'Content-Type': 'application/json-rpc'}
        result = {}
        postdata = json.dumps(data)
        for i in range(0, retry):
            try:
                httpclient = httplib.HTTPConnection(HOST, 80, timeout=30)
                httpclient.request("POST", URL, postdata, HEADER)
                response = httpclient.getresponse()
                if response.status == 200:
                    responsedic = json.loads(response.read())
                    if 'error' in responsedic.keys():
                        print 'zabbix response error :  %s' % responsedic['error']
                        continue
                    result = responsedic['result']
                    break
                else:
                    print 'zabbix response status: %s' % response.status
                    print 'zabbix response info : %s ' % response.read()
            except Exception as e:
                exc = traceback.format_exc()
                print 'zabbix exception info : %s' % e
                print 'zabbix exception info : %s' % exc
                print 'request url : %s ' % URL
                print 'request host : %s ' % HOST
                print 'request head : %s ' % HEADER
                print 'request PostDate :%s ' % postdata
        return result

    def _getToken(self):
        """
            获取Token，api_method为user.login
            _queryZabbix(jsondic):return:
                {
                    "jsonrpc": "2.0",
                    "result": "0424bd59b807674191e7d77572075f33",
                    "id": 1
                }
        """
        jsondic = {"jsonrpc": "2.0",
                   "method": "user.login",
                   "params": {
                       "user": zabbix_api_username,
                       "password": zabbix_api_password
                   },
                   "id": 1
                   }
        response = self._queryZabbix(jsondic)
        if response:
            self.token = response

    def usergroup_create(self, name, userids=None):
        """
            创建zabbix用户组
        :param name: 组名
        :param userids: 添加的用户id，可以为str和list
        :return:
        """
        jsondic = {
                    "jsonrpc": "2.0",
                    "method": "usergroup.create",
                    "params": {
                        "name": name,
                        #
                        # "rights": {
                        #     "permission": 0,
                        #     "id": "2"
                        # },
                    },
                    "auth": self.token,
                    "id": 1}
        # 判断是否添加用户
        if userids !=None:
            jsondic["params"]["userids"] = userids
        return self._queryZabbix(jsondic)


    def user_addmedia(self):
        """
            用户添加示警媒介
            _queryZabbix(jsondic):return:
                {
                    "jsonrpc": "2.0",
                    "result": {
                        "mediaids": [
                            "12",
                            "13"
                        ]
                    },
                    "id": 1
                }
        """
        jsondic = {"jsonrpc": "2.0",
                    "method": "user.addmedia",
                    "params": {
                                  "users": [
                                      {
                                          "userid": "1"
                                      },
                                      {
                                          "userid": "2"
                                      }
                                  ],
                                  "medias": {
                                      "mediatypeid": "1",
                                      "sendto": "support@company.com",
                                      "active": 0,
                                      "severity": 63,
                                      "period": "1-7,00:00-24:00"
                                  }
                              },
                    "auth": "038e1d7b1735c6a5436ee9eae095879e",
                    "id": 1}
        pass

    def user_deletemedia(self):
        """
            用户删除示警媒介
            :return:
                {
                    "jsonrpc": "2.0",
                    "result": {
                        "mediaids": [
                            "11",
                            "13"
                        ]
                    },
                    "id": 1
                }
        """
        jsondic = {"jsonrpc": "2.0",
            "method": "user.deletemedia",
            "params": [
                "11",
                "13"
            ],
            "auth": "3a57200802b24cda67c4e4010b50c065",
            "id": 1}
        pass




















































































    def getallhost(self):
        """
            获取所有主机列表
        :return:
        """
        hostdic = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                # "output": [
                #     "hostid",
                #     "host"
                # ],
                "selectInterfaces": [
                    "interfaceid",
                    "ip"
                ]
            },
            "id": 2,
            "auth": self.token
        }
        return self._queryZabbix(hostdic)

    def delhost(self, hosts):
        """
            删除指定主机
        :param hosts:
        :return:
        """
        hostids = []
        for h in self.getallhost():
            if h['host'] in hosts:
                hostids.append(h['hostid'])

        hostdic = {
            "jsonrpc": "2.0",
            "method": "host.delete",
            "params": hostids,
            "auth": self.token,
            "id": 1
        }
        self._queryZabbix(hostdic)

    def disablehost(self, hosts):
        """

        :param hosts:
        :return:
        """
        for h in self.getallhost():
            if h['host'] in hosts:
                hostids = h['hostid']

                hostdic = {
                    "jsonrpc": "2.0",
                    "method": "host.update",
                    "params": {"hostid": hostids,
                               "status": 1
                               },
                    "auth": self.token,
                    "id": 1
                }
                self._queryZabbix(hostdic)

    def enablehost(self, hosts):
        """

        :param hosts:
        :return:
        """
        for h in self.getallhost():
            if h['host'] in hosts:
                hostids = h['hostid']

                hostdic = {
                    "jsonrpc": "2.0",
                    "method": "host.update",
                    "params": {"hostid": hostids,
                               "status": 0
                               },
                    "auth": self.token,
                    "id": 1
                }
                self._queryZabbix(hostdic)

    def __update_macros(self, **kwargs):

        hostdic = {
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": {
                "hostid": kwargs['hostid'],
                "macros": kwargs['macros']
            },
            "auth": self.token,
            "id": 1
        }
        return self._queryZabbix(hostdic)

    def createhost(self, **kwargs):
        '''

        :param hostinfo:
                {'hostname':'hostname',
                    'ip':'ip',
                    'groupid':'groupid',
                    'templateid':'templateid'
                    }
        :return:
            if add seccess .
        '''
        hostdic = {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": kwargs['host'],
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": kwargs['ipaddr'].strip(),
                        "dns": '',
                        "port": "10050"
                    }
                ],
                "groups": kwargs['groupids'],
                "templates": kwargs['templateidlist'],

            },
            "auth": self.token,
            "id": 1
        }
        res = self._queryZabbix(hostdic)
        if 'macros' in kwargs.keys():
            kwargs['hostid'] = res['hostids'][0]
            self.__update_macros(**kwargs)

    def getTemplate(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        hostdic = {
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "filter": kwargs
            },
            "auth": self.token,
            "id": 1
        }
        return self._queryZabbix(hostdic)

    def getitems(self, hostids, key_):
        itemdic = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": "extend",
                "hostids": hostids,
                "search": {
                    "key_": key_
                },
                "sortfield": "name"
            },
            "auth": self.token,
            "id": 1
        }
        return self._queryZabbix(itemdic)

    def getitemshistory(self, time_from=0, time_till=0, itemids=None, history=0):
        if not itemids:
            itemids = []
        historydic = {"jsonrpc": "2.0",
                      "method": "history.get",
                      "params": {"history": history,
                                 "itemids": itemids,
                                 "time_from": time_from,
                                 "time_till": time_till,
                                 "output": "extend"},
                      "auth": self.token,
                      "id": 0}
        return self._queryZabbix(historydic)

    def getitemlastdaystat(self, itemids, history=0):
        result = {}
        time_from = int((date.today() - timedelta(days=1)).strftime('%s'))
        time_still = int(date.today().strftime('%s'))
        tlist = self.getitemshistory(time_from=time_from, time_till=time_still, itemids=itemids,
                                     history=history)
        # print len(tlist)
        for l in tlist:
            value = float(l['value'])
            itemid = l['itemid']
            if itemid not in result.keys():
                result[itemid] = []
            result[itemid].append(value)
        for id in result.keys():
            minv = min(result[id])
            avgv = sum(result[id]) / len(result[id])
            result[id] = (minv, avgv)
            # return -1, -1
        return result

    def queryTest(self, date):

        return self._queryZabbix(date)

    def getallgroups(self):
        groupdic = {
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "extend",
                "filter": {
                    "name": [
                        "Zabbix servers",
                        "Linux servers",
                        "ADS",
                        "DEV",
                        "Discovered hosts",
                        "dns",
                        "DP",
                        "dubbo-test",
                        "ELB",
                        "ELK",
                        "EMR",
                        "Huodong",
                        "MEMCACHE",
                        "Mikoomi templates",
                        "Mongo",
                        "ms-shop",
                        "MySQL DB Group",
                        "nli",
                        "RDS service",
                        "Redis",
                        "search",
                        "shop",
                        "Shop-seller",
                        "Social",
                        "Swoole",
                        "test-cluster",
                        "zk",
                        "zookeeper"
                    ]
                }
            },
            "auth": self.token,
            "id": 1
        }


if __name__ == '__main__':
    hosts = {}
    zbx = zabbix()
    for t in zbx.getTemplate():
        print t
        print t['name'], t['templateid']





