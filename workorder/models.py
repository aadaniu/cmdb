# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


from opmanage.models import Serverline_info


# Create your models here.


class Host_WorkOrder_info(models.Model):
    """
        主机工单
    """
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
    type_choices = (
        ('2c4m','2核4G'),
        ('4c8m','4核8G'),
    )
    domain_choices = (
        ('whysdomain.com','whysdomain.com'),
        ('why.com','why.com')
    )

    host_workorder_id = models.AutoField(primary_key=True)              # id
    submit_time = models.DateField(auto_now_add=True)                   # 提交时间
    submit_user = models.CharField(max_length=20)                       # 提交用户
    subject = models.CharField(max_length=30)                           # 主题
    git_code = models.CharField(max_length=30)                          # git仓库
    describe = models.CharField(max_length=30)                          # 描述
    serverline_name = models.ForeignKey('opmanage.Serverline_info')     # 业务线,host,elb和domain都依赖于此
    cloud_type = models.CharField(max_length=30, choices=cloud_choices) # 云主机类型


    # host
    apply_type = models.CharField(max_length=30, choices=apply_choices) # 申请主机业务类型
    host_type = models.CharField(max_length=30, choices=type_choices)   # 主机类型
    host_number = models.PositiveSmallIntegerField()                    # 申请主机数量
    pubipaddr = models.CharField(max_length=30, choices=t_or_f_choices) # 是否要求外网IP
    disk = models.CharField(max_length=30)                              # 磁盘大小 new

    # monitor
    monitor_url = models.CharField(max_length=30)                       # 需监控url

    # log
    nginx_log_save = models.CharField(max_length=30,choices=t_or_f_choices)     # 是否需要上传nginx log
    app_log_save_pwd = models.CharField(max_length=30, blank=True, null=True)                          # 需要上传app日志pwd new
    nginx_log_elk = models.CharField(max_length=30,choices=t_or_f_choices)      # 是否需要elb nginx log new
    app_log_elk_pwd = models.CharField(max_length=30, blank=True, null=True)                           # 需要elk的app日志pwd new
    # lb
    internal_lb = models.CharField(max_length=30, choices=t_or_f_choices)           # 是否创建内网ELB new
    internal_role = models.CharField(max_length=30, blank=True)                                 # 内网路由规则
    internet_facing_lb = models.CharField(max_length=30, choices=t_or_f_choices)    # 是否创建外网ELB new
    internet_facing_role = models.CharField(max_length=30, blank=True, null=True)                          # 外网路由规则
    # domain
    internal_domain = models.CharField(max_length=30, choices=t_or_f_choices)       # 是否创建内网域名 new
    internet_facing_domain = models.CharField(max_length=30, choices=t_or_f_choices)# 是否创建外网域名 new
    domain = models.CharField(max_length=30, choices=domain_choices, blank=True, null=True)                # 域名

    # workorder_status = models.ManyToManyField('Status_WorkOrder_info', request=False)  # 工单处理流程


class Status_WorkOrder_info(models.Model):
    """
        主机工单状态
    """
    status_workorder_id = models.AutoField(primary_key=True)                # id
    submit_time = models.DateTimeField(auto_now=True)                       # 处理时间
    attribute_workorder = models.ManyToManyField('Host_WorkOrder_info')     # 所属工单
    step_num = models.CharField(max_length=30)                              # 步骤
    step_message = models.CharField(max_length=255)                         # 处理过程
    step_status = models.CharField(max_length=30, default='wait op exec')   # 处理结果
    step_url = models.CharField(max_length=255, null=True)                  # 用于人工处理的url



class Serverline_WorkOrder_info(models.Model):
    """
        业务线工单表
    """
    submit_time = models.DateField(auto_now_add=True)                   # 提交时间
    submit_user = models.CharField(max_length=20)                       # 提交用户
    serverline_name = models.CharField(max_length=30)                   # 业务线
    serverline_leader = models.ForeignKey('opmanage.User_info')         # 业务线负责人
    describe = models.CharField(max_length=30)                          # 描述
