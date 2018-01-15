# -*- coding: utf-8 -*-
# 2018-01-02
# by why

# from salt import client
#
# def saltapi(tgt, fun, arg, tgt_type='glob'):
#     """
#
#         根据salt api官方文档
#         https://docs.saltstack.com/en/latest/ref/clients/
#
#         tgt_type --
#             The type of tgt. Allowed values:
#             glob - Bash glob completion - Default
#             pcre - Perl style regular expression
#             list - Python list of hosts
#             grain - Match based on a grain comparison
#             grain_pcre - Grain comparison with a regex
#             pillar - Pillar data comparison
#             pillar_pcre - Pillar data comparison with a regex
#             nodegroup - Match on nodegroup
#             range - Use a Range server for matching
#             compound - Pass a compound match string
#             ipcidr - Match based on Subnet (CIDR notation) or IPv4 address.
#         tgt_type -- Changed in version 2017.7.0: Renamed from expr_form to tgt_type
#
#     """
#     saltconnection = client.LocalClient()
#     saltconnection.cmd(tgt, fun, arg=(), timeout=None, tgt_type='glob', ret='', jid='', full_return=False, kwarg=None)



import urllib2, urllib, json
import requests
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class SaltAPI(object):


    def __init__(self, url, username, password):
        self.__url = url.rstrip('/')
        self.__user = username
        self.__password = password
        self.__token_id = self.saltLogin()


    def saltLogin(self):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        headers = {'X-Auth-Token': ''}
        url = self.__url + '/login'
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        try:
            token = content['return'][0]['token']
            return token
        except KeyError:
            raise KeyError


    def postRequest(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib2.Request(url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content


    def masterToMinionContent(self, tgt, fun, arg):
        '''
            Master控制Minion，返回的结果是内容，不是jid；
            目标参数tgt是一个如下格式的字符串：'*' 或 'zhaogb-201'
        '''
        if tgt == '*':
          params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        else:
          params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg, 'expr_form': 'list'}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        result = content['return'][0]
        return result
    def allMinionKeys(self):
        '''
            返回所有Minion keys；
            分别为 已接受、待接受、已拒绝；
            :return: [u'local', u'minions_rejected', u'minions_denied', u'minions_pre', u'minions']
        '''
        params = {'client': 'wheel', 'fun': 'key.list_all'}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        minions_rej = content['return'][0]['data']['return']['minions_rejected']
        # return minions, minions_pre, minions_rej
        return minions


    def actionKyes(self, keystrings, action):
        '''
            对Minion keys 进行指定处理；
            :param keystrings: 将要处理的minion id字符串；
            :param action: 将要进行的处理，如接受、拒绝、删除；
            :return:
            {"return": [{"tag": "salt/wheel/20160322171740805129", "data": {"jid": "20160322171740805129", "return": {}, "success": true, "_stamp": "2016-03-22T09:17:40.899757", "tag": "salt/wheel/20160322171740805129", "user": "zhaogb", "fun": "wheel.key.delete"}}]}
        '''
        func = 'key.' + action
        params = {'client': 'wheel', 'fun': func, 'match': keystrings}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret


    def acceptKeys(self, keystrings):
        '''
            接受Minion发过来的key；
            :return:
        '''
        params = {'client': 'wheel', 'fun': 'key.accept', 'match': keystrings}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret


    def deleteKeys(self, keystrings):
        '''
            删除Minion keys；
            :param node_name:
            :return:
        '''
        params = {'client': 'wheel', 'fun': 'key.delete', 'match': keystrings}
        obj = urllib.urlencode(params)
        content = self.postRequest(obj)
        ret = content['return'][0]['data']['success']
        return ret