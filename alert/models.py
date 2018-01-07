# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class HistoryAlert_info(models.Model):
    """
        报警表
    """

    clock = models.CharField(max_length=30)                             # 时间戳
    subject = models.CharField(max_length=256)                          # 报警信息
    event_id = models.CharField(max_length=30)                          # event id
    trigger_id = models.CharField(max_length=30)                        # trigger id
    trigger_status = models.CharField(max_length=30)                    # trigger状态
    cause = models.CharField(max_length=30, null=True)                  # 原因
    solution = models.CharField(max_length=30, null=True)               # 处理方式
    alert_status = models.CharField(max_length=30)                      # 处理情况
    def __unicode__(self):
        return self.subject


class ClosedTrigger_info(models.Model):
    """
        已关闭trigger表
    """

    trigger_id = models.CharField(max_length=30)                        # trigger id
    close_time = models.CharField(max_length=30)                        # 需要关闭多久

