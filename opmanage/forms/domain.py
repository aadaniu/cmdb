# -*- coding: utf-8 -*-
# 2017-12-21
# by why


from django import forms

from opmanage.models import Domain_info

class AddDomainForm(forms.ModelForm):
    """
        添加域名表单
    """
    class Meta:
        model = Domain_info
        # 表示该模型的全部字段都被表单使用
        fields = '__all__'
        labels = {
            'name': u'主机记录',
            'domain': u'域名',
            'types': u'记录类型',
            'value': u'记录值',
            'describe': u'描述',
            'backend_type': u'后端主机类型',
            'serverline': u'业务线',
        }


class DelDomainForm(forms.Form):
    """
        删除域名表单
    """
    name = forms.CharField(label=u'待删除记录')
    domain = forms.CharField(label=u'记录所属域名')

    def clean(self):
        cleaned_data = super(DelDomainForm, self).clean()
        name = cleaned_data.get('name')
        domain = cleaned_data.get('domain')
        if check_nameanddomain_exit(name, domain) == False:
            self.add_error('name', '域名记录不存在')


def check_nameanddomain_exit(name, domain):
    pass
