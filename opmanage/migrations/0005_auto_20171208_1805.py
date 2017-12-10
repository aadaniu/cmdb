# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-08 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opmanage', '0004_auto_20171203_1659'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host_info',
            old_name='type',
            new_name='cloud',
        ),
        migrations.AddField(
            model_name='host_info',
            name='ipaddr',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='host_info',
            name='status',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='host_info',
            name='types',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
