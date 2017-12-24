# -*- coding: utf-8 -*-
# 2017-12-24
# by why

from django import forms

from opmanage.models import Department_info


class AddDepartmentForm(forms.ModelForm):
    class Meta:
        model = Department_info
        # 表示该模型的全部字段都被表单使用
        fields = '__all__'
        labels = {
            'department_name': u'部门名称',
            'department_leader': u'部门负责人',
            'department_email': u'部门邮箱组',
        }


class DelDepartmentForm(forms.Form):
    department_name = forms.CharField(label=u'待删除部门')


    def clean(self):
        cleaned_data = super(DelDepartmentForm, self).clean()
        department_name = cleaned_data.get('department_name')
        if checkdepartment_exit(department_name) == False:
            self.add_error('department_name', '部门不存在')


def checkdepartment_exit(department_name):
    """
        检测department是否存在
    :param department_name:
    :return:
    """
    checkdepartment_exit_status = Department_info.objects.filter(department_name=department_name).count()
    if checkdepartment_exit_status == 1:
        return True
    else:
        return False