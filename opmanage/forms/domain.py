# -*- coding: utf-8 -*-
# 2017-12-21
# by why


from django.forms import ModelForm, forms

from opmanage.models import Domain_info

class AddDomainForm(ModelForm):
    class Meta:
        model = Domain_info
        # 表示该模型的全部字段都被表单使用
        fields = '__all__'


class DelDomainForm(ModelForm):
    class Meta:
        model = Domain_info
        # 表示该模型的全部字段都被表单使用
        fields = ['name',]
