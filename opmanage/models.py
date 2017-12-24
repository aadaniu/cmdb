# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


cloud_choices = (
        ('aws',u'亚马逊云'),
        ('qcloud',u'腾讯云'),
        ('aliyun',u'阿里云'),
    )

class Department_info(models.Model):
    """
        部门表
    """
    department_name = models.CharField(max_length=30,unique=True)       # 部门名称
    department_leader = models.CharField(max_length=30)                 # 部门leader
    department_email = models.EmailField()                              # 部门email
    def __unicode__(self):
        return self.department_name


class User_info(models.Model):
    """
        用户表
    """
    username = models.CharField(max_length=20,unique=True)  # 用户名
    password = models.CharField(max_length=20)              # 密码
    phone = models.CharField(max_length=15)                 # 电话
    department = models.ForeignKey('Department_info')       # 部门
    email = models.EmailField()                             # 邮箱
    auth = models.CharField(max_length=20)                  # cmdb权限
    jumper = models.CharField(max_length=1)                 # 跳板机
    vpn = models.CharField(max_length=1)                    # vpn
    zabbix = models.CharField(max_length=1)                 # zabbix账号
    git = models.CharField(max_length=1)                    # git账号
    jenkins = models.CharField(max_length=1)                # jenkins账号
    entrytime = models.DateField(auto_now_add=True)         # 入职时间
    def __unicode__(self):
        return self.username


class Serverline_info(models.Model):
    """
        业务线
    """
    serverline_name = models.CharField(max_length=30,unique=True)       # 业务线名称
    serverline_leader = models.CharField(max_length=30)                 # 业务线负责人
    serverline_op_leader = models.CharField(max_length=30)              # 业务线运维负责人
    department = models.ForeignKey('Department_info')                   # 业务线所属部门
    createtimme = models.DateField(auto_now_add=True)                   # 业务线创建时间
    def __unicode__(self):
        return self.serverline_name


class Host_info(models.Model):
    """
        主机
    """
    host_name = models.CharField(max_length=30)                  # 主机
    pro_ipaddr = models.GenericIPAddressField()             # 内网IP地址
    pub_ipaddr = models.GenericIPAddressField()             # 公网IP地址，new
    cloud = models.CharField(max_length=30, choices=cloud_choices)                 # 云主机类型
    types = models.CharField(max_length=30)                 # 内存cpu
    status = models.CharField(max_length=30)                # 运行状态
    serverline = models.ForeignKey('Serverline_info')           # ，new


class Lb_info(models.Model):
    """
        负载均衡
    """

    types_choices = (
        ('internal',u'内网'),
        ('internet-facing', u'外网'),
    )

    name = models.CharField(max_length=30)              # 名称
    cname = models.CharField(max_length=30)             # 用于CNAME解析的域名
    ipaddr = models.GenericIPAddressField()             # 用于A记录解析的IP地址
    backend_host = models.ManyToManyField('Host_info')  # 后端主机
    role_from_port = models.CharField(max_length=30)    # LB上端口
    role_to_port = models.CharField(max_length=30)      # 后端主机
    cloud = models.CharField(max_length=30, choices=cloud_choices)          # 云厂商
    types = models.CharField(max_length=30, choices=types_choices)          # 内外网
    serverline = models.ForeignKey('Serverline_info')       # 业务线，new

class Domain_info(models.Model):
    """
        域名
    """
    backend_types_choices = (
        ('lb',u'负载均衡器'),
        ('host',u'主机'),
        ('other',u'其他')
    )
    types_choices = (
        ('A',u'A记录'),
        ('CNAME','CNAME')
    )

    serverline = models.ForeignKey('Serverline_info')   # ，new
    name = models.CharField(max_length=128)  # 主机记录
    domain = models.CharField(max_length=64) # 域名
    types = models.CharField(max_length=30, choices=types_choices)        # 记录类型
    value = models.CharField(max_length=128) # 记录值
    describe = models.CharField(max_length=128) # 备注
    backend_type = models.CharField(max_length=30, choices=backend_types_choices)   # 后端资源类型，new



