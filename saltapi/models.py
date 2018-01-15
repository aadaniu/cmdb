# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class SaltReturns_info(models.Model):
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
