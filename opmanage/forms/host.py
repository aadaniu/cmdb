# -*- coding: utf-8 -*-
# 2017-12-13
# by why

from django import forms


from opmanage.models import Host_info, Serverline_info

cloud_choices = (
        ('aws',u'亚马逊云'),
        ('qcloud',u'腾讯云'),
        ('aliyun',u'阿里云'),
    )
t_or_f_choices = (
    ('t','是'),
    ('f', '否')
)
type_choices = (
    ('2c4m','2核4G'),
    ('4c8m','4核8G'),
)

# class AddHostForm(forms.ModelForm):
#     class Meta:
#         model = Host_info
#         # 表示该模型的全部字段都被表单使用
#         fields = '__all__'
#
#         labels = {
#             'host_name': u'主机名',
#             'pro_ipaddr': u'内网IP地址',
#             'pub_ipaddr': u'外网IP地址',
#             'cloud': u'云厂商',
#             'types': u'主机型号',
#             'status': u'运行状态',
#             'serverline': u'业务线',
#         }


class AddHostForm(forms.Form):

    host_workorder_id = forms.CharField(max_length=30)
    step_num = forms.CharField(max_length=30)
    cloud_type = forms.CharField(max_length=30,
                                 widget=forms.Select(attrs={'class': "form-control select"}, choices=cloud_choices),
                                 label=u'云厂商')
    host_type = forms.CharField(max_length=30,
                                widget=forms.Select(attrs={'class': "form-control select"}, choices=type_choices),
                                label=u'主机型号')
    host_number = forms.CharField(max_length=30,
                                  widget=forms.TextInput(attrs={'class': "form-control"}),
                                  label=u'申请主机数量')
    pubipaddr = forms.CharField(max_length=30,
                                widget=forms.Select(attrs={'class': "form-control select"},
                                                    choices=t_or_f_choices), label=u'是否需要外网IP')
    disk = forms.CharField(max_length=30,
                           widget=forms.TextInput(attrs={'class': "form-control"}),
                           label=u'磁盘大小')

    def __init__(self, *args, **kwargs):
        super(AddHostForm, self).__init__(*args, **kwargs)
        self.fields['serverline'] = forms.CharField(max_length=30,
                                                    widget=forms.Select(attrs={'class': "form-control select"}, choices=Serverline_info.objects.values_list('serverline_name','serverline_name')),
                                                    label=u'所属业务线')


class DelHostForm(forms.Form):
    host_name = forms.CharField(max_length=30, label='主机名')

class RenameHostForm(forms.Form):
    host_name = forms.CharField(max_length=30)
    new_name = forms.CharField(max_length=30)

class UpdownHostForm(forms.Form):
    host_name = forms.CharField(max_length=30)
    status = forms.CharField(max_length=30)


class UpdataHostForm(forms.ModelForm):
    class Meta:
        model = Host_info
        # 表示该模型的全部字段都被表单使用
        fields = '__all__'

        labels = {
            'host_name': u'主机名',
            'pro_ipaddr': u'内网IP地址',
            'pub_ipaddr': u'外网IP地址',
            'cloud': u'云厂商',
            'types': u'主机型号',
            'status': u'运行状态',
            'serverline': u'业务线',
        }

        # 防止被选中
        # widgets = {
        #     'cloud': forms.widgets.Select(attrs={'disabled': 'disabled'}),
        # }


class GetHostForm(forms.Form):
    host_name = forms.CharField(max_length=30, label='主机名')