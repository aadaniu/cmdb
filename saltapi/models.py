# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class SaltReturns_info(models.Model):
    """
        salt 执行结果返回值
    """
    exec_time = models.DateTimeField()
    tgt = models.CharField(max_length=100)
    fun = models.CharField(max_length=50)
    str_kwarg = models.CharField(max_length=255)
    tgt_type = models.CharField(max_length=15)
    result = models.TextField(db_column='result')
    # class Meta:
    #     managed = False
    #     db_table = 'salt_returns'
    def __unicode__(self):
        return u'%s %s %s %s' % (self.tgt_type, self.tgt, self.fun, self.str_kwarg)


class HostGroup(models.Model):
    """
        自定义主机组，serverline自动创建主机组
    """
    group_name = models.CharField(max_length=30)
    host_info = models.ManyToManyField('opmanage.host_info', through='HostToHostgroup')
    def __unicode__(self):
        return self.group_name
