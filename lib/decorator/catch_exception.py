# -*- coding: utf-8 -*-
# 2017-11-29
# by why

import logging
import traceback

from lib.log.api_exception import MyException,UnknownException

info_log = logging.getLogger("info")
error_log = logging.getLogger("error")
debug_log = logging.getLogger("debug")

def catch_exception(func):
    """异常捕获装饰器
        1、捕获类函数出现的异常，并记录日志。
        2、提取函数真实名称。
    """

    def _catch_exception(*args, **kwargs):

        try:
            if "_get_real_func_name" in kwargs.keys():
                return -3, func.__name__
            status, result = func(*args, **kwargs)

        except MyException as e:
            error_log.error(e.error_code)
            error_log.error(e.error_info)
            return e.error_code, e.error_msg
        except Exception as e:
            my_class_name = args[0].__class__.__name__
            my_name = func.__name__
            exc = traceback.format_exc(e)
            error_log.error(str(e))
            error_log.error(exc)
            error_log.error("In class function : %s.%s" % (my_class_name, my_name))
            ue = UnknownException()
            return ue.error_code, "%s.%s" % (my_class_name, my_name)
        return status, result

    return _catch_exception


def catch_func_exception(func):
    """
        捕获普通函数出现的异常，并记录日志。
    :param func:
    :return:
    """

    def _catch_exception(*args, **kwargs):
        try:

            status, result = func(*args, **kwargs)
        except MyException as e:
            error_log.error("%s:%s" % (e.error_code, e.message))
            return e.error_code, e.error_info
        except Exception as e:
            my_func_name = func.__name__
            exc = traceback.format_exc(e)
            error_log.error(str(e))
            error_log.error(exc)
            error_log.error("In function: %s" % my_func_name)
            ue = UnknownException()
            return ue.error_code, "%s" % (my_func_name,)
        return status, result

    return _catch_exception