# -*- coding: utf-8 -*-
# 2017-12-13
# by why

from django import forms

from opmanage.models import User_info



class LoginUserForm(forms.Form):
    username = forms.CharField(required=True,
                               max_length=20,
                               error_messages={'required': '用户名不能为空',
                                               'invalid': '用户名格式错误'},
                               widget=forms.TextInput(attrs={'class':'form-control',
                                                             'placeholder':"Username"}))
    password = forms.CharField(required=True,
                               max_length=20,
                               error_messages={'required': '密码不能为空',
                                               'invalid': '密码格式错误'},
                               widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                 'placeholder':"Password"}))
    nextpath = forms.CharField(required=False,)

    # py2
    def clean(self):
        cleaned_data = super(LoginUserForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if checkusername_exit(username) == False:
            self.add_error('username', '用户名不存在')
        if check_username_password(username, password) == False:
            self.add_error('password', '密码错误')



    # py3





def check_username_password(username, password):
    """
        用于检测用户名和密码是否正确
    :param username:
    :param password:
    :return:
    """
    if User_info.objects.filter(username=username,password=password).count():
        return True
    else:
        return False

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