# -*- coding: utf-8 -*-
# 2017-12-08
# by why

import json
import traceback

# from QcloudApi.qcloudapi import QcloudApi

# 腾讯云clb相关sdk文档
# https://cloud.tencent.com/document/product/214/10824
# 腾讯clb相关api接口
# https://cloud.tencent.com/document/product/214/1261

class Clb(object):
    def __init__(self):
        self._config = {
            "Region": "bj",
            "secretId": "AKIDUt9D6nfbprx0sXtHUWR9FOTWQ8e2lMI2",
            "secretKey": "mnncJo9IH4f82pRr595pNvNdkfPwJVVJ",
            "method": "post"
        }
        self._module = "lb"
        self.service = QcloudApi(self._module, self._config)

    def get_clbs(self, **kwargs):
        params = kwargs
        ret = []
        returnData = self.service.call(action="DescribeLoadBalancers", params=params)
        returnData = json.loads(returnData)
        print returnData
        assert returnData["code"] == 0

        try:
            for loadBalancer in returnData["loadBalancerSet"]:
                print loadBalancer
        except Exception as e:
            return 1, None
        return 0, ret


if __name__ == '__main__':
    clb = Clb()
    print clb.get_clbs(forward=-1)

"""
{u'codeDesc': u'Success',
u'totalCount': 3,
u'message': u'',
u'code': 0,
u'loadBalancerSet':
    [{u'lbChargePrepaid': {u'renewFlag': u'', u'period': u'0'},
    u'domain': u'', u'vpcId': 146490, u'uniqVpcId': u'vpc-omvdbifa',
    u'loadBalancerName': u'gold-goldProducerWeb', u'loadBalancerId': u'lb-f5ulxusp',
    u'subnetId': 1,
    u'loadBalancerVips': [u'140.143.48.94'], u'log': u'', u'projectId': 0, u'forward': 1,
    u'snat': False, u'status': 1, u'unLoadBalancerId': u'lb-f5ulxusp',
    u'internetAccessible': {u'internetChargeType': u'', u'internetMaxBandwidthOut': u'0'},
    u'expireTime': u'0000-00-00 00:00:00', u'openBgp': 0, u'createTime': u'2017-11-29 17:46:25',
    u'isolatedTime': u'0000-00-00 00:00:00', u'isolation': 0, u'loadBalancerType': 2,
    u'lbChargeType': u'', u'statusTime': u'2017-11-30 12:05:27', u'rsRegionInfo': {u'region': u'bj', u'vpcId': u'vpc-omvdbifa'}},
    余下数据
    {u'lbChargePrepaid': {u'renewFlag': u'', u'period': u'0'}, u'domain': u'', u'vpcId': 146490, u'uniqVpcId': u'vpc-omvdbifa', u'loadBalancerName': u'gold-goldUserWeb', u'loadBalancerId': u'lb-rbuzrm5f', u'subnetId': 1, u'loadBalancerVips': [u'140.143.179.211'], u'log': u'', u'projectId': 0, u'forward': 1, u'snat': False, u'status': 1, u'unLoadBalancerId': u'lb-rbuzrm5f', u'internetAccessible': {u'internetChargeType': u'', u'internetMaxBandwidthOut': u'0'}, u'expireTime': u'0000-00-00 00:00:00', u'openBgp': 0, u'createTime': u'2017-11-29 17:08:48', u'isolatedTime': u'0000-00-00 00:00:00', u'isolation': 0, u'loadBalancerType': 2, u'lbChargeType': u'', u'statusTime': u'2017-11-30 10:30:57', u'rsRegionInfo': {u'region': u'bj', u'vpcId': u'vpc-omvdbifa'}}, {u'lbChargePrepaid': {u'renewFlag': u'', u'period': u'0'}, u'domain': u'', u'vpcId': 146490, u'uniqVpcId': u'vpc-omvdbifa', u'loadBalancerName': u'disconf', u'loadBalancerId': u'lb-3uvzz2dh', u'subnetId': 36487, u'loadBalancerVips': [u'10.40.8.6'], u'log': u'', u'projectId': 0, u'forward': 0, u'snat': False, u'status': 1, u'unLoadBalancerId': u'lb-3uvzz2dh', u'internetAccessible': {u'internetChargeType': u'', u'internetMaxBandwidthOut': u'0'}, u'expireTime': u'0000-00-00 00:00:00', u'openBgp': 0, u'createTime': u'2017-11-27 15:21:41', u'isolatedTime': u'0000-00-00 00:00:00', u'isolation': 0, u'loadBalancerType': 3, u'lbChargeType': u'', u'statusTime': u'2017-11-28 11:11:58', u'rsRegionInfo': {u'region': u'bj', u'vpcId': u'vpc-omvdbifa'}}]}
"""