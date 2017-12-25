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
            'name': u'lb名称',
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
    name = forms.CharField(label=u'待删除记录')

    def clean(self):
        cleaned_data = super(DelLbForm, self).clean()
        name = cleaned_data.get('name')
        if check_name_exit(name) == False:
            self.add_error('name', '负载均衡器不存在')


def check_name_exit(name):
    pass
