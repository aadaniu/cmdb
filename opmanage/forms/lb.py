# -*- coding: utf-8 -*-
# 2017-12-18
# by why

from django import forms

from opmanage.models import Lb_info

class AddLbForm(forms.ModelForm):
    class Meta:
        model = Lb_info
        # 表示该模型的全部字段都被表单使用
        fields = '__all__'
        labels = {
            'lb_name': u'lb名称',
            'cname': u'cname',
            'ipaddr': u'a记录ip',
            'backend_host': u'后端主机',
            'role_from_port': u'lb端口',
            'role_to_port': u'后端主机端口',
            'cloud': u'云类型',
            'types': u'内外网类型',
            'serverline': u'业务线',
        }


class DelLbForm(forms.Form):
    lb_name = forms.CharField(label=u'待删除记录')

    def clean(self):
        cleaned_data = super(DelLbForm, self).clean()
        lb_name = cleaned_data.get('lb_name')
        if check_name_exit(lb_name) == False:
            self.add_error('name', 'LB不存在')


class UpdataLbForm(forms.ModelForm):
    class Meta:
        model = Lb_info
        # 表示该模型的全部字段都被表单使用
        fields = '__all__'
        labels = {
            'lb_name': u'lb名称',
            'cname': u'cname',
            'ipaddr': u'a记录ip',
            'backend_host': u'后端主机',
            'role_from_port': u'lb端口',
            'role_to_port': u'后端主机端口',
            'cloud': u'云类型',
            'types': u'内外网类型',
            'serverline': u'业务线',
        }


class GetLbForm(forms.Form):
    every_page_sum_choices = (
        (20, 20),
        (30, 30),
        (50, 50),
    )
    search_lb = forms.CharField(label=u'搜素LB',max_length=30)
    # pages = forms.CharField(label=u'页数', max_length=30)
    # every_page_sum = forms.CharField(label=u'每页显示行数', max_length=2, widget=forms.widgets.Select(choices=every_page_sum_choices))

def check_name_exit(name):
    pass
