# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-28 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoryAlert_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clock', models.CharField(max_length=30)),
                ('subject', models.CharField(max_length=256)),
                ('event_id', models.CharField(max_length=30)),
                ('trigger_id', models.CharField(max_length=30)),
                ('trigger_status', models.CharField(max_length=30)),
                ('cause', models.CharField(max_length=30, null=True)),
                ('solution', models.CharField(max_length=30, null=True)),
                ('alert_status', models.CharField(max_length=30)),
            ],
        ),
    ]
