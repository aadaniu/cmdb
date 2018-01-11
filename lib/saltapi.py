# -*- coding: utf-8 -*-
# 2018-01-02
# by why

# from salt import client
#
# def saltapi(tgt, fun, arg, tgt_type='glob'):
#     """
#
#         根据salt api官方文档
#         https://docs.saltstack.com/en/latest/ref/clients/
#
#         tgt_type --
#             The type of tgt. Allowed values:
#             glob - Bash glob completion - Default
#             pcre - Perl style regular expression
#             list - Python list of hosts
#             grain - Match based on a grain comparison
#             grain_pcre - Grain comparison with a regex
#             pillar - Pillar data comparison
#             pillar_pcre - Pillar data comparison with a regex
#             nodegroup - Match on nodegroup
#             range - Use a Range server for matching
#             compound - Pass a compound match string
#             ipcidr - Match based on Subnet (CIDR notation) or IPv4 address.
#         tgt_type -- Changed in version 2017.7.0: Renamed from expr_form to tgt_type
#
#     """
#     saltconnection = client.LocalClient()
#     saltconnection.cmd(tgt, fun, arg=(), timeout=None, tgt_type='glob', ret='', jid='', full_return=False, kwarg=None)
