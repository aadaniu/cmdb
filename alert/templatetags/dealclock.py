# -*- coding: utf-8 -*-
# 2018-01-09
# by why

import time
from django import template

# 创建模板库实例
register = template.Library()

# 注册过滤器
@register.filter(is_safe=True)
def dealclock(clock):
    format_clock = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(clock)))
    return format_clock
