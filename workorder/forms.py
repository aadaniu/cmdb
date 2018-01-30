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
            'git_code': u'git仓库',
            'describe': u'描述',
            'serverline_name': u'所属业务线',
            'cloud_type': u'云厂商',

            # host
            'apply_type': u'主机业务类型',
            'host_type': u'主机型号(cpu和内存)',
            'host_number': u'申请主机数量',
            'pubipaddr': u'是否需要外网IP',
            'disk' : u'磁盘大小',
            # monitor
            'monitor_url': u'待监控url',
            # log
            'nginx_log_save': u'是否需要保存nginx日志到cos（或者s3）',
            'app_log_save_pwd': u'是否需要保存业务日志到cos（或者s3）的日志路径',
            'nginx_log_elk': u'是否需要上传nginx日志到elk',
            'app_log_elk_pwd': u'需要上传业务日志到elk的日志路径',
            # lb
            'internal_lb': u'是否创建内网ELB',
            'internal_role': u'内网路由规则',
            'internet_facing_lb': u'是否创建外网ELB',
            'internet_facing_role': u'外网路由规则',

            # domain
            'internal_domain': u'是否创建内网域名',
            'internet_facing_domain': u'是否创建外网域名',
            'domain': u'申请域名',

        }
        # 添加样式
        widgets = {
            'subject': forms.TextInput(attrs={'class': "form-control"}),
            'git_code': forms.TextInput(attrs={'class': "form-control"}),
            'describe': forms.widgets.Textarea(attrs={'rows': 5, 'class': "form-control", 'placeholder': u'详细描述'}),
            'serverline_name': forms.Select(attrs={'class': "form-control select"}),
            'cloud_type': forms.Select(attrs={'class': "form-control select"}),
            # host
            'apply_type': forms.Select(attrs={'class': "form-control select"}),
            'host_type': forms.Select(attrs={'class': "form-control select"}),
            'host_number': forms.TextInput(attrs={'class': "form-control spinner_default"}),
            'pubipaddr': forms.Select(attrs={'class': "form-control select"}),
            'disk': forms.TextInput(attrs={'class': "form-control"}),
            # monitor
            'monitor_url': forms.TextInput(attrs={'class': "tagsinput"}),
            # log
            'nginx_log_save': forms.Select(attrs={'class': "form-control select"}),
            'app_log_save_pwd': forms.TextInput(attrs={'class': "tagsinput"}),
            'nginx_log_elk': forms.Select(attrs={'class': "form-control select"}),
            'app_log_elk_pwd': forms.TextInput(attrs={'class': "tagsinput"}),
            # lb
            'internal_lb': forms.Select(attrs={'class': "form-control select"}),
            'internal_role': forms.TextInput(attrs={'class': "tagsinput"}),
            'internet_facing_lb': forms.Select(attrs={'class': "form-control select"}),
            'internet_facing_role': forms.TextInput(attrs={'class': "tagsinput"}),
            # domain
            'internal_domain': forms.Select(attrs={'class': "form-control select"}),
            'internet_facing_domain': forms.Select(attrs={'class': "form-control select"}),
            'domain': forms.Select(attrs={'class': "form-control select", "data-live-search": "true"})
        }


    # 前端显示默认值设置
    # def __init__(self, *args, **kwargs):
    #     super(AddHostWorkOrderForm, self).__init__(*args, **kwargs)
    #     self.initial["cloud_type"] = 'aws'
    #     self.initial["apply_type"] = 'php'
    #     self.initial["pubipaddr"] = 't'
    #     self.initial["monitor_url"] = '/heart.php'
    #     self.initial["host_number"] = 1




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