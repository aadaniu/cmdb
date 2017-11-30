# -*- coding: utf-8 -*-
# 2017-11-30
# by why

from django import forms

class UserForm(forms.Form):
    username = forms.CharField(required=True,max_length=20,error_messages={'required': '用户名不能为空','invalid': '用户名格式错误'})
    password = forms.CharField(required=True,max_length=20,error_messages={'required': '密码不能为空','invalid': '密码格式错误'})

class AddUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    email = forms.CharField()
    auth = forms.CharField()
    jumper = forms.CharField()
    vpn = forms.CharField()
    phone = forms.CharField()
    department = forms.CharField()
    ccj_admin = forms.CharField()
    cct_admin = forms.CharField()





