# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-30 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workorder', '0002_auto_20180130_0131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status_workorder_info',
            name='submit_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
