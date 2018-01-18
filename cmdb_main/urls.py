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
from django.conf.urls.static import static
from django.conf import settings


from opmanage.views import index, user, test, test_zabbix, host, lb, domain, department, serverline
from alert.views import *
from saltapi.views import *
from workorder.views import *

urlpatterns = [
    # url(r'^admin/', admin.site.urls),


    ###################Test#############################
    url(r'^test/$', test.test),                     # 测试主页面
    url(r'^testcmdb/$', test.test_cmdbbase),        # 测试cmdbbase
    url(r'^test/adduesr', test.insert_data),        # 测试添加用户
    url(r'^test/addhost', test.insert_host),        # 测试添加主机
    url(r'^test/sendtable', test.sendtable),        # 测试发送表格邮件
    url(r'^test/sendmail', test.send),              # 测试发送邮件
    url(r'^test/zabbix', test_zabbix.test_zabbix),  # 测试zabbix
    url(r'^test/jenkins', test.testjenkins),        # 测试jenkins
    url(r'^test/log', test.log_test),               # 测试log


    ###################Index#############################
    url(r'^index/login/', index.login),             # 登录
    url(r'^index/logout/', index.logout),           # 退出
    url(r'^index/index/', index.index),             # 主页
    ###################User#############################
    url(r'^user/adduser/', user.add_user),                      # 添加用户
    url(r'^user/deluser/', user.del_user),                      # 删除用户
    url(r'^user/updatauser/',user.updata_user),                 # 更新用户
    url(r'^user/getuser/',user.get_user),                       # 查询用户
    url(r'^user/getmessage/',user.get_message),                 # 获取用户
    url(r'^user/updatauserpassword/',user.updata_user_password),# 更新用户名密码
    ###################Department#############################
    url(r'^department/adddepartment/',department.add_department),       # 添加部门
    url(r'^department/deldepartment/',department.del_department),       # 删除部门
    url(r'^department/getdepartment/',department.get_department),       # 获取部门
    url(r'^department/updatadepartment/',department.updata_department), # 更新部门
    ###################Serverline#############################
    url(r'^serverline/addserverline/',serverline.add_serverline),       # 添加业务线
    url(r'^serverline/delserverline/',serverline.del_serverline),       # 删除业务线
    url(r'^serverline/getserverline/',serverline.get_serverline),       # 获取业务线
    url(r'^serverline/updataserverline/',serverline.updata_serverline), # 更新业务线
    ###################Host#############################
    url(r'^host/addhost/',host.add_host),       # 添加主机
    url(r'^host/delhost/',host.del_host),       # 删除主机
    url(r'^host/updatahost/',host.updata_host), # 更新主机
    url(r'^host/gethost/',host.get_host),       # 获取主机
    url(r'^host/renamehost/', host.rename_host),# 更名主机
    url(r'^host/updownhost/', host.updown_host),# 删除主机
    ###################LB#############################
    url(r'^lb/addlb/',lb.add_lb),           # 添加LB
    url(r'^lb/dellb/',lb.del_lb),           # 删除LB
    url(r'^lb/updatalb/', lb.updata_lb),    # 更新LB
    url(r'^lb/getlb/',lb.get_lb),           # 获取LB
    ###################Domain#############################
    url(r'^domain/adddomain/',domain.add_domain),       # 添加域名
    url(r'^domain/deldomain/',domain.del_domain),       # 删除域名
    url(r'^domain/getdomain/',domain.get_domain),       # 获取域名
    url(r'^domain/updatadomain/',domain.updata_domain), # 更新域名


    ###################Alert##############################
    url(r'^alert/gethistoryalert/',get_historyalert),       # 获取历史报警信息
    url(r'^alert/get_lastday_alert/',get_last_day_alert),   # 获取近一天的所有报警
    url(r'^alert/get_last10_alert/',get_last_10_alert),     # 获取最近10条报警
    url(r'^alert/get_closed_alert/',get_closed_alert),      # 获取已经关闭的报警
    url(r'^alert/editalert/',edit_alert),                   # 完善报警处理流程
    url(r'^alert/addalert/',add_alert),                     # zabbix action添加alert接口
    url(r'^alert/closetrigger/',close_trigger),             # zabbix trigger关闭接口





    ###################Salt##############################
    url(r'^saltapi/saltrun/',exec_cmd),                     # 获取历史报警信息
    url(r'^saltapi/saltpillar/', exec_cmd),                 # 主机标签

    ###################WorkOrder##############################
    url(r'^workorder/add_host_workorder/',add_host_workorder),                  # 创建主机工单
    url(r'^workorder/add_serverline_workorder/',add_serverline_workorder),      # 创建业务线工单
    url(r'^workorder/check_serverline_workorder/',check_serverline_workorder),  # 审核业务线工单
]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

