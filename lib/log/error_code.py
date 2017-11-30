# -*- coding: utf-8 -*-
# 2017-11-29
# by why

import json
import traceback
from datetime import datetime
from datetime import date

# os.chdir(sys.path[0])

import logging

error_log = logging.getLogger("error")

Error_code = {
    '100001': 'Authenticated failed.%s',
    '100002': '%s',
    '100003': '%s',
    '200001': 'Executed sql on db is error, error code : %s.',
    '300001': "Can't find a valid record %s.",
    '400001': 'The parameter value is not allowed to be empty.Empty parameter list:%s.',
    '400002': 'The parameter type is wrong.Wrong parameter list:%s.',
    '400003': 'The parameter value is invalid.Invalid parameter list:%s.',
    '400004': 'The parameter is invalid.Invalid parameter list:%s.',
    '400005': "The parameter is invalid.Can't contain single quotes and double quotess.%s",
    '500005': 'Unknow error had happened.Please call 4321 for help.Info:%s.',
    '600001': 'Call api failed:%s.',
    '600002': 'Call rt api failed:%s',
    '600003': 'Operation deny access.%s',
    '601000': 'Comment ID do not exist %s .',
    '602000': 'Redis ID do not exist %s .',
    '602001': 'Redis ID was repeat %s .',
    '602002': 'Redis name was repeat %s .',
    '602003': 'Master Id is same as redis id  %s .',
    '603000': 'Mc ID do not exist %s .',
    '603001': 'Mc ID was repeat %s .',
    '603002': 'Mc name was repeat %s .',
    '603003': 'Master Id is same as mc id  %s .',
    '604000': 'Nginx name is not exist %s',
    '604001': 'Nginx id is  not exist %s',
    '605000': 'Fpm name is not exist %s',
    '605001': 'Fpm id is not exist %s',
    '606000': 'Create ec2 failed %s',
    '606001': 'Ec2 not exist %s',
    '607001': 'Java service not exist %s',
    '608000': 'Get deploy msg failed %s',
    '608001': 'Deploy msg create failed %s',
    '608002': 'Deploy msg delete failed %s',
    '608003': 'Deploy msg update failed %s',
    '609000': 'Get tag msg failed %s',
    '609001': 'Update tag msg failed %s',
    '609002': 'Delete tag msg failed %s',
    '610000': 'Product point not exist %s',
    '700001': 'The page is not found.',
    '800001': '%s'
}


def show_error_code(self, error_code, extra=None, **kwargs):
    """
    格式化错误信息。
    :param self:
    :param error_code:
    :param extra:
    :param kwargs:
    :return:
    """
    error_code = str(error_code)
    error_msg = Error_code.get(error_code, "Unknown Error code : %s")
    if extra:
        error_msg = error_msg % extra
    uri = self.request.uri
    resource_and_interface = uri.split('?')[0]
    message = {"request": resource_and_interface, "error_code": error_code, "error": error_msg}
    return_msg = {"status": -1, "result": message}
    result = json.dumps(return_msg, ensure_ascii=False)
    # logger.error(result)
    self.write(result)


def show_correct_result(self, message, **kwargs):
    return_msg = {"status": 0, "result": message}
    result = json.dumps(return_msg, ensure_ascii=False, cls=JsonExtendEncoder)
    # print result
    self.write(result)


def show_result(self, ret_code, message, **kwargs):
    try:
        if ret_code == 0:
            show_correct_result(self, message)
        else:
            show_error_code(self, ret_code, message)
    except Exception, e:
        error_log.error("%s:%s" % (ret_code, message))
        error_log.error(str(e))
        error_log.error(traceback.format_exc())
        # print str(e)


class JsonExtendEncoder(json.JSONEncoder):
    """
        This class provide an extension to json serialization for datetime/date.
    """

    def default(self, o):
        """
            provide a interface for datetime/date
        """
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, o)


if __name__ == '__main__':
    show_result(None, 1, 'message test.')
