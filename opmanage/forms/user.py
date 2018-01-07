# -*- coding: utf-8 -*-
# 2017-12-13
# by why

from django import forms

from opmanage.models import User_info

tf = [('t', '创建'), ('2', '不创建')]
cmdb_auth = ((1, "user"),(10,"resource"))
department_choice = ((1, "user"),(10,"resource"))#Department_info.objects.values_list("id", "department_name")


# class AddUserForm(forms.Form):
#     """
#         添加用户表单
#     """
#     username = forms.CharField(label=u'用户名')
#     password = forms.CharField(label=u'密码', widget=forms.PasswordInput)
#     phone = forms.CharField(label=u'联系电话')
#     department = forms.CharField(label=u'部门',widget=forms.widgets.Select(choices=department_choice))
#     auth = forms.MultipleChoiceField(label=u'权限', widget=forms.CheckboxSelectMultiple(),choices=cmdb_auth)
#     jumper = forms.ChoiceField(label=u'跳板机账户',widget=forms.RadioSelect, choices=tf)
#     vpn = forms.ChoiceField(label=u'VPN账户',widget=forms.RadioSelect, choices=tf)
#     zabbix = forms.ChoiceField(label=u'zabbix账户',widget=forms.RadioSelect, choices=tf)
#     git = forms.ChoiceField(label=u'git账户',widget=forms.RadioSelect, choices=tf)
#     jenkins = forms.ChoiceField(label=u'jenkins账户',widget=forms.RadioSelect, choices=tf)
#
    # def clean(self):
    #     cleaned_data = super(AddUserForm, self).clean()
    #     username = cleaned_data.get('username')
    #     if checkusername_exit(username) == True:
    #         self.add_error('username', '用户名已存在')

class AddUserForm(forms.ModelForm):
    class Meta:
        model = User_info
        # 表示该模型的全部字段都被表单使用
        fields = '__all__'
        extend = ['entrytime',]

        labels = {
            'username': u'用户名',
            'password': u'密码',
            'phone': u'电话',
            'department': u'部门',
            'email': u'邮箱',
            'auth': u'cmdb权限',
            'vpn': u'vpn账号',
            'zabbix': u'zabbix账号',
            'git': u'git账号',
            'jenkins': u'jenkins账号',
        }

    def clean(self):
        cleaned_data = super(AddUserForm, self).clean()
        username = cleaned_data.get('username')
        if checkusername_exit(username) == True:
            self.add_error('username', '用户名已存在')




class DelUserForm(forms.Form):
    """
        删除用户表单
    """
    username = forms.CharField(label=u'待删除用户名')

    def clean(self):
        cleaned_data = super(DelUserForm, self).clean()
        username = cleaned_data.get('username')
        if checkusername_exit(username) == False:
            self.add_error('username', '用户名不存在')

class UpdataUserForm(forms.ModelForm):
    """
        更新用户表单
    """
    class Meta:
        model = User_info
        # 表示该模型的全部字段都被表单使用
        fields = '__all__'
        extend = ['entrytime',]

        labels = {
            'username': u'用户名',
            'password': u'密码',
            'phone': u'电话',
            'department': u'部门',
            'email': u'邮箱',
            'auth': u'cmdb权限',
            'vpn': u'vpn账号',
            'zabbix': u'zabbix账号',
            'git': u'git账号',
            'jenkins': u'jenkins账号',
        }


class GetUserForm(forms.Form):
    """
        获取用户表单
    """
    username = forms.CharField(label=u'用户名')


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