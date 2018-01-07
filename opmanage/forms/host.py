# -*- coding: utf-8 -*-
# 2017-12-13
# by why

from django import forms


from opmanage.models import Host_info

class AddHostForm(forms.ModelForm):
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