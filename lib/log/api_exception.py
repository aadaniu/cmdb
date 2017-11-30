# -*- coding: utf-8 -*-
# 2017-11-29
# by why

from lib.log.error_code import Error_code

class MyException(Exception):
    def __init__(self, error_code, msg=""):
        self.__error_code = error_code
        self.__info = msg
        self.__data = Error_code[self.error_code] % msg if msg else Error_code[self.error_code]

    def __str__(self):  # 相当于 str(#)
        return self.__data

    @property
    def error_msg(self):
        return self.__data

    @property
    def error_code(self):
        return self.__error_code

    @property
    def error_info(self):
        return self.__info


class UserDefinedException(MyException):
    """用户自定义exception"""

    def __init__(self, msg):
        super(UserDefinedException, self).__init__('800001', msg)


class CommentServiceIdDonotExsitException(MyException):
    def __init__(self, msg):
        super(CommentServiceIdDonotExsitException, self).__init__('601000', msg)


class EmptyParameterException(MyException):
    def __init__(self, msg):
        super(EmptyParameterException, self).__init__('400001', msg)


class ErrorParameterTypeException(MyException):
    def __init__(self, msg):
        super(ErrorParameterTypeException, self).__init__('400002', msg)


class InvalidParameterValueException(MyException):
    def __init__(self, msg):
        super(InvalidParameterValueException, self).__init__('400003', msg)


class UnknownException(MyException):
    def __init__(self):
        super(UnknownException, self).__init__("500005", "yy")


class MysqlErrorException(MyException):
    def __init__(self, message):
        super(MysqlErrorException, self).__init__('200001', message)


class OperationDenyException(MyException):
    def __init__(self, msg):
        super(OperationDenyException, self).__init__('600003', msg)


class RedisIdNotExistException(MyException):
    def __init__(self, msg):
        super(RedisIdNotExistException, self).__init__('602000', msg)


class RedisIdRepeatException(MyException):
    def __init__(self, msg):
        super(RedisIdRepeatException, self).__init__('602001', msg)


class RedisNameRepeatException(MyException):
    """redis name 重复异常 """

    def __init__(self, msg):
        super(RedisNameRepeatException, self).__init__('602002', msg)


class RedisIdRepeatWithMasterIdException(MyException):
    """redis 同主库ID相同异常"""

    def __init__(self, msg):
        super(RedisIdRepeatWithMasterIdException, self).__init__('602003', msg)


class McIdNotExistException(MyException):
    def __init__(self, msg):
        super(McIdNotExistException, self).__init__('603000', msg)


class McIdRepeatException(MyException):
    def __init__(self, msg):
        super(McIdRepeatException, self).__init__('603001', msg)


class McNameRepeatException(MyException):
    """Mc name 重复异常 """

    def __init__(self, msg):
        super(McNameRepeatException, self).__init__('603002', msg)


class McIdRepeatWithMasterIdException(MyException):
    """Mc 同主库ID相同异常"""

    def __init__(self, msg):
        super(McIdRepeatWithMasterIdException, self).__init__('603003', msg)


class NginxNameRepeatException(MyException):
    """
    nginx name exist
    """

    def __init__(self, msg):
        super(NginxNameRepeatException, self).__init__('604000', msg)


class NginxIdRepeatException(MyException):
    """
    nginx id exist
    """

    def __init__(self, msg):
        super(NginxIdRepeatException, self).__init__('604001', msg)


class FpmNameRepeatException(MyException):
    """
    fpm name exist
    """

    def __init__(self, msg):
        super(FpmNameRepeatException, self).__init__('605000', msg)


class FpmIdRepeatException(MyException):
    """
    fpm id exist
    """

    def __init__(self, msg):
        super(FpmIdRepeatException, self).__init__('605001', msg)


class Ec2CreateException(MyException):
    """ec2 创建异常"""

    def __init__(self, msg):
        super(Ec2CreateException, self).__init__('606000', msg)


class Ec2NotExistException(MyException):
    """ec2 主机不存在异常"""

    def __init__(self, msg):
        super(Ec2NotExistException, self).__init__('606001', msg)


class Ec2DeleteException(MyException):
    """ec2 删除异常"""

    def __init__(self, msg):
        super(Ec2DeleteException, self).__init__('606002', msg)


class JavaServiceNotExistException(MyException):
    """java 服务未定义异常"""

    def __init__(self, msg):
        super(JavaServiceNotExistException, self).__init__('607001', msg)


class GetDeployMsgException(MyException):
    """查询服务部署信息异常"""

    def __init__(self, msg):
        super(GetDeployMsgException, self).__init__('608000', msg)


class DeployMsgCreateException(MyException):
    """创建服务部署信息异常"""

    def __init__(self, msg):
        super(DeployMsgCreateException, self).__init__('608001', msg)


class DeployMsgDeleteException(MyException):
    """删除服务部署信息异常"""

    def __init__(self, msg):
        super(DeployMsgDeleteException, self).__init__('608002', msg)


class DeployMsgUpdateException(MyException):
    """删除服务部署信息异常"""

    def __init__(self, msg):
        super(DeployMsgUpdateException, self).__init__('608003', msg)


class GetTagMsgException(MyException):
    """查询服务部署信息异常"""

    def __init__(self, msg):
        super(GetTagMsgException, self).__init__('609000', msg)


class UpdateTagMsgException(MyException):
    """更新服务部署信息异常"""

    def __init__(self, msg):
        super(UpdateTagMsgException, self).__init__('609001', msg)


class DeleteTagMsgException(MyException):
    """删除服务部署信息异常"""

    def __init__(self, msg):
        super(DeleteTagMsgException, self).__init__('609002', msg)


class CreateTagMsgException(MyException):
    """创建服务部署信息异常"""

    def __init__(self, msg):
        super(CreateTagMsgException, self).__init__('609003', msg)


class ProductPointNotExistException(MyException):
    """产品线节点不存在异常"""

    def __init__(self, msg):
        super(ProductPointNotExistException, self).__init__('610000', msg)


if __name__ == '__main__':
    # raise ConnectDBFailException
    ue = UnknownException()
    print ue.error_code
    raise EmptyParameterException()
