# -*- coding: utf-8 -*-
# 2017-12-02
# by why

import random


class RandomStr(object):
    def __init__(self):
        pass

    @classmethod
    def make(cls, length=8):
        """
            生成固定长度随机字符串。
        :param length:
            字符串长度。
        :return:
            string
        """
        str = "abcdefghijklmnopqrstuvwxyz0123456789"
        return ''.join(random.sample(str, length))


    @classmethod
    def make_id(cls, title="", length=8):
        """
            生成固定长度随机字符串。
        :param title:
            字符串头
        :param length:
            字符串长度。
        :return:
            string
        """
        str = "abcdefghijklmnopqrstuvwxyz0123456789"
        return title + '-' + ''.join(random.sample(str, length))
