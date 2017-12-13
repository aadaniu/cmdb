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

from opmanage.views import index, user, test, test_zabbix

urlpatterns = [
    url(r'^test/$', test.test),# 测试主页面
    url(r'^test/adduesr', test.insert_data),# 测试添加用户
    url(r'^test/addhost', test.insert_host),# 测试添加主机
    url(r'^test/sendtable', test.sendtable),# 测试发送表格邮件
    url(r'^test/sendmail', test.send),# 测试发送邮件
    url(r'^test/zabbix', test_zabbix.test_zabbix),# 测试zabbix
    # url(r'^admin/', admin.site.urls),
    url(r'^index/login/', index.login),# 登录
    url(r'^index/logout/', index.logout),# 退出
    url(r'^index/index/', index.index),# 主页
    url(r'^user/adduser/', user.add_user),# 添加用户
    url(r'^user/deluser/', user.del_user),# 删除用户
    url(r'^user/updatauser/',user.updata_user),# 更新用户
    url(r'^user/getuser/',user.get_user),# 查询用户
    url(r'^user/getmessage/',user.get_message),# 获取用户
    url(r'^user/updatauserpassword/',user.updata_user_password),# 更新用户名密码
    # url(r'^login/', index.login),# 登录
    # url(r'^logout/', index.logout),# 退出
    # url(r'^index/', index.index),# 主页
    # url(r'^adduser/', user.add_user),# 添加用户
    # url(r'^deluser/', user.del_user),# 删除用户
    # url(r'^updatauser/',user.updata_user),# 更新用户
    # url(r'^getuser/',user.get_user),# 查询用户
    # url(r'^getmessage/',user.get_message),# 获取用户
    # url(r'^updatauserpassword/',user.updata_user_password),# 更新用户名密码
]

