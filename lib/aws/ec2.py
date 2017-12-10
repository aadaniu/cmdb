# -*- coding: utf-8 -*-
# 2017-12-08
# by why

from lib.aws.aws import Aws
import json

class Ec2(Aws):
    def __init__(self):
        """
            初始化ec2
        :return:
        """
        super(Ec2, self).__init__(client_name="ec2")
        self._aws_response = {}
        self._aws_ec2_list = []
        self._request_aws()

    def _request_aws(self, retry=3, *args, **kwargs):
        """
            请求aws接口，获取ec2基本信息
            client.describe_instances文档 参考 http://boto3.readthedocs.io/en/latest/reference/services/ec2.html#EC2.Client.describe_instances
        :param retry:重试次数
        :param args:
        :param kwargs:
        :return:
        """
        for i in range(0, retry):
            try:
                self._aws_response = self.client.describe_instances(Filters=[])
            except Exception as e:
                pass
            break


    def get_ec2(self):
        """提取ec2主要信息。"""
        result = []
        self._request_aws()

        response = self._aws_response
        try:
            for r in response["Reservations"]:
                for i in r["Instances"]:
                    name = None
                    tags = {}
                    if "Platform" in i.keys():
                        continue
                    ipaddr = "127.0.0.1"
                    if "PrivateIpAddress" in i.keys():
                        ipaddr = i["PrivateIpAddress"]
                    ec2_id = i["InstanceId"]
                    state_name = i["State"]["Name"]
                    state_code = i["State"]["Code"] % 256
                    if "Tags" in i.keys():
                        for tag in i["Tags"]:
                            tags[tag["Key"]] = tag["Value"]
                            if tag["Key"] == u"Name":
                                name = tag["Value"]
                    if name is None or name == "":
                        continue
                    instance_type = i["InstanceType"]
                    result.append({
                        "ec2_id": ec2_id,
                        "ipaddr": ipaddr,
                        "name": name,
                        "state_name": state_name,
                        "state_code": state_code,
                        "instance_type": instance_type,
                        "tags": json.dumps(tags)
                    })
        except Exception as e:
            return 1, None
        return 0, result


if __name__ == "__main__":
    ee = Ec2()
    ec2s = ee.get_ec2()
    print len(ec2s), ec2s[0]

