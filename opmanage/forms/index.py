# -*- coding: utf-8 -*-
# 2017-11-30
# by why

from django import forms

from opmanage.models import User_info

def checkusername_exit(username):
    """
        检查用户名是否存在
    :param username:
    :return:
    """
    check_userexit_status = User_info.objects.filter(username=username).count()
    if check_userexit_status == 1:
        return True
    else:
        return False

class LoginUserForm(forms.Form):
    username = forms.CharField(required=True,max_length=20,error_messages={'required': '用户名不能为空','invalid': '用户名格式错误'})
    password = forms.CharField(required=True,max_length=20,error_messages={'required': '密码不能为空','invalid': '密码格式错误'})

    # py2
    def clean(self):
        cleaned_data = super(LoginUserForm, self).clean()
        username = cleaned_data.get('username')
        if checkusername_exit(username) == False:
            self.add_error('username', '用户名不存在')

    # py3