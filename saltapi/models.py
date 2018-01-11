# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class accect_cmd(models.Model):
    command = models.CharField(max_length=50, unique=True, verbose_name=u'命令')
    status = models.CharField(max_length=20, verbose_name=u'状态')
    def __unicode__(self):
        return u'{0} {1}'.format(self.command, self.status)


class SaltReturns(models.Model):
    fun = models.CharField(max_length=50)
    jid = models.CharField(max_length=255)
    return_field = models.TextField(db_column='return')
    success = models.CharField(max_length=10)
    full_ret = models.TextField()
    alter_time = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'salt_returns'
    def __unicode__(self):
        return u'%s %s %s' % (self.jid, self.id, self.return_field)


class record(models.Model):
    time = models.DateTimeField(u'时间', auto_now_add=True)
    comment = models.CharField(max_length=128, blank=True, default='', null=True, verbose_name=u"记录")
    def __unicode__(self):
        return u'%s %s' % (self.time, self.comment)