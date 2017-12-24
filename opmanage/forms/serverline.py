# -*- coding: utf-8 -*-
# 2017-12-24
# by why


from django import forms

from opmanage.models import Serverline_info


class AddServerlineForm(forms.ModelForm):
    """
        添加Serverline表单
    """
    class Meta:
        model = Serverline_info
        # 表示该模型的全部字段都被表单使用
        fields = '__all__'

        labels = {
            'serverline_name': u'业务线名称',
            'serverline_leader': u'业务线负责人',
            'serverline_op_leader': u'业务线运维负责人',
            'department': u'所属部门',
        }


class DelServerlineForm(forms.Form):
    """
        删除Serverline表单
    """
    serverline_name = forms.CharField()

    def clean(self):
        cleaned_data = super(DelServerlineForm, self).clean()
        serverline_name = cleaned_data.get('serverline_name')
        if checkserverline_exit(serverline_name) == False:
            self.add_error('serverline_name', '业务线不存在')







def checkserverline_exit(serverline_name):
    """
        检测serverline是否存在
    :param serverline_name:
    :return:
    """
    check_serverlineexit_status = Serverline_info.objects.filter(serverline_name=serverline_name).count()
    if check_serverlineexit_status == 1:
        return True
    else:
        return False
