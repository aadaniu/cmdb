# -*- coding: utf-8 -*-
# 2017-12-08
# by why

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest

# 阿里云sdk文档
# https://help.aliyun.com/document_detail/53090.html?spm=5176.product52507.3.1.i1W0Ht

client = AcsClient(
       "LTAIYzQMhMOO0tnG",
       "dgntZ7ZSDC7vV7OsVhBBnMeLlwV8Om",
       "cn-hongkong"
   );

request = DescribeInstancesRequest.DescribeInstancesRequest()
request.set_PageSize(10)

response = client.do_action_with_exception(request)
print response

# 返回结果

"""
{"PageNumber":1,
"TotalCount":1,
"PageSize":10,
"RequestId":"BCD41DBC-7236-4359-9833-6BFDCB887680",
"Instances":
    {"Instance":
        [{"InnerIpAddress":{"IpAddress":[]},
        "ImageId":"centos_6_08_64_40G_alibase_20170710.vhd",
        "InstanceTypeFamily":"ecs.xn4",
        "VlanId":"",
        "NetworkInterfaces":
            {"NetworkInterface":[{"NetworkInterfaceId":"eni-j6c64dij3tdrz275oepj"}]},
            "InstanceId":"i-j6cgrz5db6q2esz9zooe",
            "EipAddress":{"IpAddress":"","AllocationId":"","InternetChargeType":""},
            "InternetMaxBandwidthIn":500,"ZoneId":"cn-hongkong-c",
            "InternetChargeType":"PayByBandwidth",
            "SpotStrategy":"NoSpot",
            "StoppedMode":"Not-applicable",
            "SerialNumber":"0f829652-9d9d-40dc-b445-8dd9e589154a","
            IoOptimized":true,
            "Memory":1024,
            "Cpu":1,
            "VpcAttributes":{"NatIpAddress":"","PrivateIpAddress":{"IpAddress":["172.31.51.204"]},"VSwitchId":"vsw-j6can769pzygllm4smkgx","VpcId":"vpc-j6c3ma6s2vhp00cd5dcvm"},
            "InternetMaxBandwidthOut":1,
            "DeviceAvailable":true,
            "SecurityGroupIds":{"SecurityGroupId":["sg-j6c64dij3tdrz26wlusy"]},
            "SaleCycle":"",
            "SpotPriceLimit":0.0,
            "AutoReleaseTime":"",
            "InstanceName":"why",
            "Description":"",
            "ResourceGroupId":"",
            "OSType":"linux",
            "OSName":"CentOS  6.8 64位",
            "InstanceNetworkType":"vpc",
            "PublicIpAddress":{"IpAddress":["47.91.228.125"]},
            "HostName":"iZj6cgrz5db6q2esz9zooeZ",
            "InstanceType":"ecs.xn4.small",
            "CreationTime":"2017-08-11T10:23Z",
            "Status":"Running",
            "ClusterId":"",
            "Recyclable":false,
            "RegionId":"cn-hongkong",
            "GPUSpec":"",
            "OperationLocks":{"LockReason":[]},
            "InstanceChargeType":"PrePaid",
            "GPUAmount":0,"ExpiredTime":"2018-08-11T16:00Z"}
        ]
    }
}
"""


