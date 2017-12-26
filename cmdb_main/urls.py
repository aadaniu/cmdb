# -*- coding: utf-8 -*-
"""cmdb_main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from opmanage.views import index, user, test, test_zabbix, host, lb, domain, department, serverline

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^test/$', test.test),# 测试主页面
    url(r'^testcmdb/$', test.test_cmdbbase),# 测试cmdbbase
    url(r'^test/adduesr', test.insert_data),# 测试添加用户
    url(r'^test/addhost', test.insert_host),# 测试添加主机
    url(r'^test/sendtable', test.sendtable),# 测试发送表格邮件
    url(r'^test/sendmail', test.send),# 测试发送邮件
    url(r'^test/zabbix', test_zabbix.test_zabbix),# 测试zabbix
    url(r'^test/jenkins', test.testjenkins),  # 测试jenkins
    url(r'^test/log', test.log_test),  # 测试log
    url(r'^index/login/', index.login),# 登录
    url(r'^index/logout/', index.logout),# 退出
    url(r'^index/index/', index.index),# 主页
    url(r'^user/adduser/', user.add_user),# 添加用户
    url(r'^user/deluser/', user.del_user),# 删除用户
    url(r'^user/updatauser/',user.updata_user),# 更新用户
    url(r'^user/getuser/',user.get_user),# 查询用户
    url(r'^user/getmessage/',user.get_message),# 获取用户
    url(r'^user/updatauserpassword/',user.updata_user_password),# 更新用户名密码
    url(r'^host/addhost/',host.add_host),# 添加主机
    url(r'^host/delhost/',host.del_host),# 删除主机
    url(r'^host/renamehost/', host.rename_host),# 更名主机
    url(r'^host/updownhost/', host.updown_host),# 删除主机
    url(r'^lb/addlb/',lb.add_lb),# 添加LB
    url(r'^lb/dellb/',lb.del_lb),# 删除LB
    url(r'^domain/adddomain/',domain.add_domain),# 添加域名
    url(r'^department/adddepartment/',department.add_department),# 添加部门
    url(r'^department/deldepartment/',department.del_department),# 删除部门
    url(r'^serverline/addserverline/',serverline.add_serverline),# 添加业务线
    url(r'^serverline/delserverline/',serverline.del_serverline),# 删除业务线
]

