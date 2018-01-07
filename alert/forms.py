# -*- coding: utf-8 -*-
# 2018-01-03
# by why


from django import forms


from alert.models import HistoryAlert_info, ClosedTrigger_info


class GetHistoryAlertForm(forms.Form):
    search_word = forms.CharField(max_length=30, label='搜索关键词')


class EditHistoryAlertForm(forms.ModelForm):
    class Meta:
        model = HistoryAlert_info
        # 表示该模型的全部字段都被表单使用
        fields = '__all__'

        labels = {
            'clock': u'报警时间',
            'subject': u'报警信息',
            'trigger_id': u'触发器id',
            'trigger_status': u'触发器状态',
            'cause': u'报警产生原因',
            'solution': u'报警处理方式',
            'alert_status': u'报警是否完全解决',
            'event_id': u'事件id',
        }

