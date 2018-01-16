# -*- coding: utf-8 -*-
# 2018-01-16
# by why

from django import forms


from workorder.models import Host_WorkOrder_info, Serverline_WorkOrder_info

class AddHostWorkOrderForm(forms.ModelForm):
    class Meta:
        model = Host_WorkOrder_info
        # 表示该模型的全部字段都被表单使用
        # fields = '__all__'
        exclude = ['submit_user']

        labels = {
            'subject': u'主题',
            'apply_type': u'申请主机类型',
            'cloud_type': u'云厂商',
            'host_type': u'主机型号',
            'pubipaddr': u'是否需要外网IP',
            'serverline': u'所属业务线',
            'monitor_url': u'待监控url',
            'git_code': u'git仓库',
            'domain': u'申请域名',
            'describe': u'描述',
        }


class AddServerlineWorkOrderForm(forms.ModelForm):
    class Meta:
        model = Serverline_WorkOrder_info
        # 表示该模型的全部字段都被表单使用
        fields = '__all__'

        labels = {
            'serverline': u'创建业务线',
            'serverline_leader': u'业务负责人',
            'describe': u'描述',
        }