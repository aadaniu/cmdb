# -*- coding: utf-8 -*-
# 2017-12-08
# by why

import boto3

# awscli和boto3的示例操作
# http://blog.csdn.net/afxcontrolbars/article/details/54634772
# 这里需要开通cmdb所在主机的权限，否则会报An error occurred (UnauthorizedOperation) when calling the DescribeInstances operation: You are not authorized to perform this operation.

class Aws(object):
    """
        Aws基类
    """
    def __init__(self, profile_name=None, client_name=None, *arg, **kwargs):
        self.profile_name = profile_name or "control-center-for-op"
        self.client_name = client_name or "ec2"
        session = boto3.Session(profile_name=self.profile_name)
        self.client = session.client(self.client_name, **kwargs)
