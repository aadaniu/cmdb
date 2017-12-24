# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-24 17:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=30, unique=True)),
                ('department_leader', models.CharField(max_length=30)),
                ('department_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Domain_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('domain', models.CharField(max_length=64)),
                ('types', models.CharField(choices=[('A', 'A\u8bb0\u5f55'), ('CNAME', 'CNAME')], max_length=30)),
                ('value', models.CharField(max_length=128)),
                ('describe', models.CharField(max_length=128)),
                ('backend_type', models.CharField(choices=[('lb', '\u8d1f\u8f7d\u5747\u8861\u5668'), ('host', '\u4e3b\u673a'), ('other', '\u5176\u4ed6')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Host_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('pro_ipaddr', models.GenericIPAddressField()),
                ('pub_ipaddr', models.GenericIPAddressField()),
                ('cloud', models.CharField(choices=[('aws', '\u4e9a\u9a6c\u900a\u4e91'), ('qcloud', '\u817e\u8baf\u4e91'), ('aliyun', '\u963f\u91cc\u4e91')], max_length=30)),
                ('types', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Lb_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('cname', models.CharField(max_length=30)),
                ('ipaddr', models.GenericIPAddressField()),
                ('role_from_port', models.CharField(max_length=30)),
                ('role_to_port', models.CharField(max_length=30)),
                ('cloud', models.CharField(choices=[('aws', '\u4e9a\u9a6c\u900a\u4e91'), ('qcloud', '\u817e\u8baf\u4e91'), ('aliyun', '\u963f\u91cc\u4e91')], max_length=30)),
                ('types', models.CharField(choices=[('internal', '\u5185\u7f51'), ('internet-facing', '\u5916\u7f51')], max_length=30)),
                ('backend_host', models.ManyToManyField(to='opmanage.Host_info')),
            ],
        ),
        migrations.CreateModel(
            name='Serverline_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serverline_name', models.CharField(max_length=30, unique=True)),
                ('serverline_leader', models.CharField(max_length=30)),
                ('serverline_op_leader', models.CharField(max_length=30)),
                ('createtimme', models.DateField(auto_now_add=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opmanage.Department_info')),
            ],
        ),
        migrations.CreateModel(
            name='User_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
                ('auth', models.CharField(max_length=20)),
                ('jumper', models.CharField(max_length=1)),
                ('vpn', models.CharField(max_length=1)),
                ('zabbix', models.CharField(max_length=1)),
                ('git', models.CharField(max_length=1)),
                ('jenkins', models.CharField(max_length=1)),
                ('entrytime', models.DateField(auto_now_add=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opmanage.Department_info')),
            ],
        ),
        migrations.AddField(
            model_name='lb_info',
            name='serverline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opmanage.Serverline_info'),
        ),
        migrations.AddField(
            model_name='host_info',
            name='serverline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opmanage.Serverline_info'),
        ),
        migrations.AddField(
            model_name='domain_info',
            name='serverline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opmanage.Serverline_info'),
        ),
    ]
