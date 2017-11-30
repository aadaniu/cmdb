# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.db import models

class User_info(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.EmailField()
    auth = models.BooleanField()
    jumper = models.BooleanField()
    vpn = models.BooleanField()
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=30)
    ccj_admin = models.BooleanField()
    cct_admin = models.BooleanField()


class Department_info(models.Model):
    name = models.CharField(max_length=30)
    leader = models.CharField(max_length=30)


class Host_info(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
