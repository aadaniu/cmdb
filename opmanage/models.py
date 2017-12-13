# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models

class User_info(models.Model):
    username = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    auth = models.CharField(max_length=20)
    jumper = models.BooleanField()
    vpn = models.BooleanField()
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=30)
    zabbix = models.BooleanField()
    kibana = models.BooleanField()


class Department_info(models.Model):
    name = models.CharField(max_length=30)
    leader = models.CharField(max_length=30)


class Host_info(models.Model):
    """
    id name IP 机型 实例状态 标签信息
    """
    name = models.CharField(max_length=30)
    ipaddr = models.CharField(max_length=30)
    cloud = models.CharField(max_length=30)
    types = models.CharField(max_length=30)
    status = models.CharField(max_length=30)

