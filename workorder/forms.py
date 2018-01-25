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
        # 标签
        labels = {
            'subject': u'主题',
            'apply_type': u'申请主机类型',
            'cloud_type': u'云厂商',
            'host_type': u'主机型号',
            'pubipaddr': u'是否需要外网IP',
            'serverline_name': u'所属业务线',
            'monitor_url': u'待监控url',
            'git_code': u'git仓库',
            'domain': u'申请域名',
            'describe': u'描述',
        }
        # 添加样式
        widgets = {
            'subject': forms.TextInput(attrs={'class': "form-control"}),
            'apply_type': forms.Select(attrs={'class': "form-control select"}),
            'cloud_type': forms.Select(attrs={'class': "form-control select"}),
            'host_type': forms.TextInput(attrs={'class': "form-control"}),
            'pubipaddr': forms.Select(attrs={'class': "form-control select"}),
            'serverline_name': forms.Select(attrs={'class': "form-control select"}),
            'monitor_url': forms.TextInput(attrs={'class': "tagsinput"}),
            'git_code': forms.TextInput(attrs={'class': "form-control"}),
            'domain': forms.TextInput(attrs={'class': "form-control"}),
            'describe': forms.widgets.Textarea(attrs={'rows': 5, 'class': "form-control", 'placeholder': u'详细描述'}),
        }

    # 前端显示默认值设置
    def __init__(self, *args, **kwargs):
        super(AddHostWorkOrderForm, self).__init__(*args, **kwargs)
        self.initial["cloud_type"] = 'aws'
        self.initial["apply_type"] = 'php'
        self.initial["pubipaddr"] = 't'
        self.initial["monitor_url"] = '/heart.php'




class AddServerlineWorkOrderForm(forms.ModelForm):
    class Meta:
        model = Serverline_WorkOrder_info
        # 表示该模型的全部字段都被表单使用
        fields = '__all__'
        exclude = ['submit_user', 'workorder_status',]

        labels = {
            'serverline_name': u'业务线名称',
            'serverline_leader': u'业务线负责人',
            'describe': u'描述',
        }

        widgets = {
            'serverline_name': forms.TextInput(attrs={'class': "form-control"}),
            'serverline_leader': forms.Select(attrs={'class': "form-control select"}),
            'describe': forms.widgets.Textarea(attrs={'rows': 5, 'class': "form-control", 'placeholder': u'详细描述'}),
        }