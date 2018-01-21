# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


from opmanage.models import Serverline_info


# Create your models here.


class Host_WorkOrder_info(models.Model):
    cloud_choices = (
        ('aws',u'亚马逊云'),
        ('qcloud',u'腾讯云'),
        ('aliyun',u'阿里云'),
    )
    apply_choices = (
        ('php','php'),
        ('java', 'java')
    )
    t_or_f_choices = (
        ('t','是'),
        ('f', '否')
    )
    submit_time = models.DateField(auto_now_add=True)                   # 提交时间
    submit_user = models.CharField(max_length=20)                       # 提交用户
    subject = models.CharField(max_length=30)                           # 主题
    apply_type = models.CharField(max_length=30, choices=apply_choices) # 申请主机类型
    cloud_type = models.CharField(max_length=30, choices=cloud_choices) # 云主机类型
    host_type = models.CharField(max_length=30)                         # 主机类型
    pubipaddr = models.CharField(max_length=30, choices=t_or_f_choices) # 是否要求外网IP
    serverline_name = models.ForeignKey('opmanage.Serverline_info')     # 业务线
    monitor_url = models.CharField(max_length=30)                       # 需监控url
    git_code = models.CharField(max_length=30)                          # git仓库
    domain = models.CharField(max_length=30)                            # 域名
    # remark = models.CharField(max_length=30)                          # 备注
    describe = models.CharField(max_length=30)                          # 描述




class Serverline_WorkOrder_info(models.Model):
    submit_time = models.DateField(auto_now_add=True)                   # 提交时间
    submit_user = models.CharField(max_length=20)                       # 提交用户
    serverline_name = models.CharField(max_length=30)                   # 业务线
    serverline_leader = models.ForeignKey('opmanage.User_info')         # 业务线负责人
    describe = models.CharField(max_length=30)                          # 描述
