# -*- coding: utf-8 -*-
# 2017-12-18
# by why

from django.forms import ModelForm, forms

from opmanage.models import Lb_info

class AddLbForm(ModelForm):
    class Meta:
        model = Lb_info
        # 表示该模型的全部字段都被表单使用
        fields = '__all__'


class DelLbForm(ModelForm):
    class Meta:
        model = Lb_info
        # 只是用列表中的字段
        fields = ['name',]