# -*- coding: utf-8 -*-
# 2017-11-30
# by why

from django import forms

class UserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    # username = forms.CharField(label='用户名：',max_length=100)
    # password = forms.CharField(label='密  码：',widget=forms.PasswordInput())



