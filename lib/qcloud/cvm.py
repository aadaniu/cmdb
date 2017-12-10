# -*- coding: utf-8 -*-
# 2017-12-08
# by why

import json
import traceback

#from QcloudApi.qcloudapi import QcloudApi

# 腾讯云sdk文档
# https://cloud.tencent.com/document/developer-resource/494/7244

class Cvm(object):
    def __init__(self):
        self._config = {
            "Region": "ap-beijing",
            "secretId": "AKIDUt9D6nfbprx0sXtHUWR9FOTWQ8e2lMI2",
            "secretKey": "mnncJo9IH4f82pRr595pNvNdkfPwJVVJ",
            "method": "post"
        }
        self._module = "cvm"
        self.service = QcloudApi(self._module, self._config)

    def get_hosts(self, **kwargs):
        params = kwargs
        ret = []
        returnData = self.service.call(action="DescribeInstances", params=params)
        returnData = json.loads(returnData)
        assert returnData["code"] == 0

        try:
            for instance in returnData["instanceSet"]:
                if instance["vpcId"] == 0:
                    continue
                if instance["lanIp"] == "":
                    continue
                state_code = 16 if instance["status"] == 2 else 32
                Ipaddr = instance["lanIp"]
                Name = instance["instanceName"]
                CvmId = instance["unInstanceId"]
                ret.append({
                    "ec2_id": CvmId,
                    "ipaddr": Ipaddr,
                    "name": Name,
                    "state_name": "no_state",
                    "state_code": state_code,
                    "instance_type": "c3.xlarge",
                    "tags": "{}"
                })
        except Exception as e:
            return 1, None
        return 0, ret


if __name__ == '__main__':
    cvm = Cvm()
    print cvm.get_hosts()

"""
{u'lanIp': u'10.40.0.2', u'instanceId': u'qcvm3b3b43754d50e195cfdf75ca88bb49e1', u'unImgId': u'img-h3gvu2j9', u'imageId': 59396, u'autoRenew': 0, u'bandwidth': 10, u'vpcId': u'bj_vpc_146490', u'deviceClass': u'VSELF_2', u'diskInfo': {u'rootType': 2, u'rootId': u'disk-oc1wb054', u'rootSize': 100}, u'subnetId': u'bj_subnet_36485', u'isVpcGateway': 0, u'uuid': u'7e4c7f49-c9cd-460e-be6f-6dc1cf129743', u'wanIpSet': [u'140.143.197.61'], u'projectId': 0, u'deadlineTime': u'2018-01-31 10:45:12', u'cvmPayMode': 1, u'zoneId': 800003, u'instanceName': u'qbj3-op-jenkins-00', u'imageType': u'\u81ea\u5b9a\u4e49\u955c\u50cf', u'status': 2, u'mem': 8, u'Region': u'bj', u'networkPayMode': 2, u'unInstanceId': u'ins-a7csfxvr', u'createTime': u'2017-11-30 10:45:08', u'zoneName': u'\u5317\u4eac\u4e09\u533a', u'statusTime': u'2017-12-08 04:40:53', u'os': u'centos6.8x86_64', u'cpu': 4}
"""