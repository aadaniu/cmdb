# -*- coding: utf-8 -*-
# 2017-12-05
# by why

import httplib
import json
import traceback

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
        getdataZabbix,根据官方文档传递参数method和params构造jsondic，通过_queryZabbix方法进行请求
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
        result = {"status": False}
        postdata = json.dumps(data)
        for i in range(0, retry):
            try:
                httpclient = httplib.HTTPConnection(HOST, 80, timeout=30)
                httpclient.request("POST", URL, postdata, HEADER)
                response = httpclient.getresponse()
                if response.status == 200:
                    responsedic = json.loads(response.read())
                    if 'error' in responsedic.keys():
                        result['data'] = responsedic['error']
                        continue
                    else:
                        result['status'] = True
                        result['data'] = responsedic['result']
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
        if response['status']:
            self.token = response['data']


    def getdataZabbix(self,method,params):
        """
            获取zabbix数据
        :param method: 对应Method reference
        :param params: parames（str，list，dic类型皆可，详见zabbix api文档）
        :return:
            result = { "status": True,
                   "data" : None
                   }
        """
        result = { "status": False,
                   "data": None
                   }
        jsondic = {
                    "jsonrpc": "2.0",
                    "method": method,
                    "params": params,
                    "auth": self.token,
                    "id": 1
        }
        try:
            response = self._queryZabbix(jsondic)
            if response['status']:
                result['status'] = True
                result['data'] = response['data']
            else:
                result['data'] = response['data']
        except Exception as e:
            result['data'] = e
        finally:
            return result

    def username_to_id(self, name):
        """
            用户名查找用户id
        :param name:
        :return:
        """
        id = None
        params = {"output": ['alias', 'userid']}
        data = self.getdataZabbix('user.get', params)
        for i in data['data']:
            if i['alias'] == name:
                id = i['userid']
                break
        return id

    def userid_to_name(self, id):
        """
            用户id查找用户名
        :param id:
        :return:
        """
        params = {"output": ['alias', 'userid'], 'userids': id}
        return self.getdataZabbix('user.get',params)['data'][0]['alias']

