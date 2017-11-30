# -*- coding: utf-8 -*-
# 2017-11-29
# by why

from django.db import models

class User_info(models.Model):
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    email = models.EmailField()
    auth = models.CharField(max_length=30)
    jumper = models.CharField(max_length=30)
    vpn = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    ccj_admin = models.CharField(max_length=30)
    cct_admin = models.CharField(max_length=30)


class Department_info(models.Model):
    name = models.CharField(max_length=30)
    leader = models.CharField(max_length=30)


class Host_info(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
