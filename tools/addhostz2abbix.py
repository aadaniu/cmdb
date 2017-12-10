# -*- coding: utf-8 -*-
# 2017-12-10
# by why

"""
    本tool用于aws上经常操作添加和删除主机。
"""

import os
import re
import pymysql

from lib.zabbix import zabbix
from lib.ec2 import ec2
from lib.elb import elb
# from lib.mysqlconnection import create_connection
from ipaddr import IPv4Network, IPv4Address
# from lib.cldns import DnsBase
# from lib.log import logged


zbx = zabbix()
# 排除主机
skiphost = ['cube-00',
            'db-ami']
# 原主机
ZBX_HOSTS = {}
# 新增主机
NEW_HOSTS = {}
# 已删除主机
ZBX_DELETE_HOSTS = []
# zabbix模板字典
ZBX_TEMPLATE = {}

# zabbix模板 gid:zabbix组id，net:主机网段，reg:前缀
groupid = {
    # 44 : dev 组。
    # 21 : shop 组。
    'dev': {'gid': '44',
            'net': ['10.30.4.0/22',
                    '10.30.12.0/22',
                    '10.30.30.0/24'],
            'reg': ['dev']
            },
    'MySQL DB Group': {'gid': '31',
                       'net': ['10.30.21.0/24'],
                       'reg': ['mysql']
                       },
    'search': {'gid': '7',
               'net': ['10.30.23.0/24'],
               'reg': []
               },
    'emr': {'gid': '2',
            'net': ['10.30.24.0/24'],
            'reg': ['emr-']
            },
    'ads': {'gid': '9',
            'net': ['10.30.25.0/24'],
            'reg': ['ads-']
            },
    'social': {'gid': '54',
               'net': ['10.30.32.0/24'],
               'reg': ['social']
               },
    'dns': {'gid': '49',
            'net': [],
            'reg': ['dns']
            },
    'dp': {'gid': '46',
           'net': [],
           'reg': ['shop-dp']
           },
    'message': {'gid': '62',
                'net': [],
                'reg': ['message']
                },
    'ms-shop': {'gid': '28',
                'net': [],
                'reg': ['ms']
                },
    'mq': {'gid': '17',
           'net': [],
           'reg': ['mq']
           },
    'nli': {'gid': '26',
            'net': [],
            'reg': ['nli']
            },
    'presell': {'gid': '60',
                'net': [],
                'reg': ['presell']
                },
    'swoole': {'gid': '18',
               'net': [],
               'reg': ['swoole']
               },
    'zk': {'gid': '40',
           'net': [],
           'reg': ['zk']
           },
    'huodong': {'gid': '15',
                'net': [],
                'reg': ['huodong']
                },
    'live': {'gid': '58',
             'net': [],
             'reg': ['live']
             },
    'look': {'gid': '56',
             'net': [],
             'reg': ['look']
             },
    'pintuan': {'gid': '61',
                'net': [],
                'reg': ['shop-productgroup']
                },
    'logstash-indexer': {'gid': '76',
                         'net': [],
                         'reg': ['lgs']
                         },
    'Redis': {'gid': '50',
              'net': [],
              'reg': ['redis']
              },
}


# 获取zabbix主机IP地址
def set_zbx_hosts():
    for h in zbx.getallhost():
        hostname = h['host']
        ipaddr = h['interfaces'][0]['ip']
        # = h['host']
        ZBX_HOSTS[hostname] = {'ipaddr': ipaddr}
    return ZBX_HOSTS


# 获取zabbix模板列表
def set_zbx_template():
    for t in zbx.getTemplate():
        ZBX_TEMPLATE[t['name']] = {'id': t['templateid']}
    return ZBX_TEMPLATE

# 获取zabbix主机所属组
def getHostGid(ip, hostname):
    ipv4 = IPv4Address(ip)
    groupids = [{"groupid": "5"}]
    for g, gi in groupid.items():
        ADD_GID = False
        for netstr in gi['net']:
            ipnet = IPv4Network(netstr)
            if ipnet.Contains(ipv4):
                groupids.append({"groupid": gi['gid']})
                ADD_GID = True
        if ADD_GID:
            continue
        for reg in gi['reg']:
            if hostname.startswith(reg):
                groupids.append({"groupid": gi['gid']})
    if len(groupids) > 1:
        del groupids[0]

    return groupids


# @logged
def get_mysql_node_info_from_db():
    result = ()
    conn = create_connection(host='10.30.21.217', port=5500, db='dpadmin')
    if conn:
        try:
            sql = 'select host,port,role,type,node_id,product_name from node_info where zabbix = 1'
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
        except Exception, e:
            print e
            result = ()
        finally:
            conn.close()
            return result

    else:
        print 'conn to db error!'
    return result


# @logged
def get_redis_node_info_from_db():
    result = ()
    conn = create_connection(host='10.30.21.217', port=5500, db='dpadmin')
    if conn:
        try:
            sql = 'select host,port,vir_port,role,type,node_id,product_name from redis_node_info where zabbix = 1'
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
        except Exception, e:
            print e
            result = ()
        finally:
            conn.close()
            return result

    else:
        print 'conn to db error!'
    return result


# @logged
def get_mc_node_info_from_db():
    result = ()
    conn = create_connection(host='10.30.21.217', port=5500, db='dpadmin')
    if conn:
        try:
            sql = 'select host,port,vir_port,role,type,node_id from mc_node_info'
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
        except Exception, e:
            print e
            result = ()
        finally:
            conn.close()
            return result

    else:
        print 'conn to db error!'
    return result


# @logged
def set_mysql_list():
    dblist = get_mysql_node_info_from_db()
    for m in dblist:
        # host,port,role,type,node_id
        ipaddr = m[0]
        port = m[1]
        role = m[2]
        dbtype = m[3]
        nodeid = m[4]
        product_name = m[5]
        macros_host = ipaddr
        macros_port = port
        macros_product = product_name
        agent_host = ipaddr
        host = "%(role)s%(port)s.%(nodeid)s.db" % {"port": port,
                                                   "nodeid": nodeid,
                                                   "role": role}
        # add default template
        templateidlist = [
            {'templateid': ZBX_TEMPLATE[u'Mysql Server Template']['id']}
        ]

        # is rds
        if dbtype == 0:
            templateidlist.append(
                {'templateid': ZBX_TEMPLATE[u'RDS template']['id']}
            )
            macros_port = 3306
            macros_host = ipaddr
            agent_host = '10.30.30.31'
            # macros_host = ipaddr
            # ipaddr = "10.30.30.31"
        # is slave
        if role != 'm':
            templateidlist.append(
                {'templateid': ZBX_TEMPLATE[u'Mysql Slave Server Template']['id']}
            )

        NEW_HOSTS[host] = {'host': host,
                           'ipaddr': agent_host,
                           'groupids': [{"groupid": "96"}],
                           'templateidlist': templateidlist,
                           'macros': [
                               {"macro": "{$MYSQL_HOST}",
                                "value": macros_host},
                               {"macro": "{$MYSQL_PORT}",
                                "value": macros_port},
                               {"macro": "{$MYSQL_PRODUCT}",
                                "value": macros_product}
                           ]
                           }
    return NEW_HOSTS


# @logged
def set_redis_list():
    # ec = ec2()
    redis_list = get_redis_node_info_from_db()
    for m in redis_list:
        # host,port,vir_port,role,type,node_id
        ipaddr = str(m[0])
        port = str(m[1])
        vPort = str(m[2])
        role = str(m[3])
        dbtype = int(m[4])
        nodeid = str(m[5])
        product_name = m[6]
        macros_host = nodeid
        macros_prot = port
        macros_product = product_name
        agent_host = ipaddr

        # is elasticache
        if dbtype == 0:
            macros_host = ipaddr
            agent_host = '10.30.30.31'

        # is slave
        if role != 'm':
            pass

        host = "%(role)s%(vPort)s.%(nodeid)s.redis" % {'role': role,
                                                       'vPort': vPort,
                                                       'nodeid': nodeid,
                                                       }

        NEW_HOSTS[host] = {'host': host,
                           'ipaddr': agent_host,
                           'groupids': [{"groupid": "85"}],
                           'templateidlist': [
                               {'templateid': ZBX_TEMPLATE[u'Redis Server Template']['id']}
                           ],
                           'macros': [
                               {"macro": "{$REDIS_HOST}",
                                "value": macros_host},
                               {"macro": "{$REDIS_PORT}",
                                "value": macros_prot},
                               {"macro": "{$REDIS_PRODUCT}",
                                "value": macros_product}
                           ]
                           }
    return NEW_HOSTS


# @logged
def set_memcache_list():
    # ec = ec2()
    mc_list = get_mc_node_info_from_db()
    for m in mc_list:
        # host,port,vir_port,role,type,node_id 区分
        ipaddr = str(m[0])
        port = str(m[1])
        vPort = str(m[2])
        role = str(m[3])
        dbtype = int(m[4])
        nodeid = str(m[5])
        macros_prot = port

        # is elasticache
        if dbtype == 0:
            macros_host = nodeid + '.wapzv2.cfg.cnn1.cache.amazonaws.com.cn'
            # macros_host = ipaddr
            agent_host = '10.30.30.31'
        else:
            macros_host = ipaddr
            agent_host = '10.30.30.31'
        # is slave
        if role != 'm':
            pass

        host = "%(vPort)s.%(nodeid)s.mc" % {'vPort': vPort,
                                            'nodeid': nodeid,
                                            }

        NEW_HOSTS[host] = {'host': host,
                           'ipaddr': agent_host,
                           'groupids': [{"groupid": "95"}],
                           'templateidlist': [
                               {'templateid': ZBX_TEMPLATE[u'Memcache Server Template']['id']}
                           ],
                           'macros': [
                               {"macro": "{$MC_HOST}",
                                "value": macros_host},
                               {"macro": "{$MC_PORT}",
                                "value": macros_prot}
                           ]
                           }
    return NEW_HOSTS


# @logged
def set_jvm_list():
    jvm_host_list = [
        ('sell-java-01-activity-dubbo', '10.30.27.226'),
        ('sell-java-02-activity-dubbo', '10.30.27.225'),
        ('sell-java-03-activity-dubbo', '10.30.24.122'),
        ('sell-java-04-activity-dubbo', '10.30.24.161'),
        ('sell-java-05-activity-dubbo', '10.30.27.57'),
        ('sell-java-03-commidity-dubbo', '10.30.24.122'),
        ('sell-java-04-commidity-dubbo', '10.30.24.161'),
        ('sell-java-05-commidity-dubbo', '10.30.27.57'),
        ('shop-malluser-A-001-tomcat', '10.30.28.167'),
        ('shop-malluser-A-002-tomcat', '10.30.28.166'),
        ('shop-malluser-A-003-tomcat', '10.30.28.168'),
        ('shop-malluser-A-001-dubbo', '10.30.28.167'),
        ('shop-malluser-A-002-dubbo', '10.30.28.166'),
        ('shop-malluser-A-003-dubbo', '10.30.28.168'),
        ('advert-web-02-adspearRouterWeb', '10.30.35.184'),
        ('advert-web-02-adspearWeb', '10.30.35.184'),
        ('advert-web-03-adspearRouterWeb', '10.30.35.185'),
        ('advert-web-03-adspearWeb', '10.30.35.185'),
        ('mallusercenter-000-tomcat', '10.30.27.227'),
        ('mallusercenter-001-tomcat', '10.30.27.156'),
        ('mallcouponuser-003-tomcat', '10.30.27.17'),
        ('mallcouponuser-004-tomcat', '10.30.27.129'),
        ('mallcouponuser-005-tomcat', '10.30.27.169'),
        ('shop-mallcoupon-001-tomcat', '10.30.27.82'),
        ('shop-mallcoupon-002-tomcat', '10.30.27.171'),
        ('mallusercenter-000-dubbo', '10.30.27.227'),
        ('mallusercenter-001-dubbo', '10.30.27.156'),
        ('mallcouponuser-003-dubbo', '10.30.27.17'),
        ('mallcouponuser-004-dubbo', '10.30.27.129'),
        ('mallcouponuser-005-dubbo', '10.30.27.169'),
        ('shop-mallcoupon-001-dubbo', '10.30.27.82'),
        ('shop-mallcoupon-002-dubbo', '10.30.27.171'),
        ('look-order-001-tomcat', '10.30.28.111'),
        ('look-order-001-dubbo', '10.30.28.111'),
        ('look-order-001-crontab', '10.30.28.111'),
        ('look-order-002-tomcat', '10.30.28.209'),
        ('look-order-002-dubbo', '10.30.28.209'),
        ('kefu-provider-A-000-kefuProvider', '10.30.34.32'),
        ('kefu-provider-A-001-kefuProvider', '10.30.34.33'),
        ('shop-java-05', '10.30.27.165'),
        ('shop-java-06', '10.30.27.243'),
        ('chuchusns-java-00', '10.30.27.93'),
        ('chuchusns-java-01', '10.30.27.120'),
        ('chuchusns-java-03', '10.30.27.28'),
        ('chuchusns-java-06', '10.30.27.106'),
        ('chuchusns-java-07', '10.30.27.198'),
        ('dwxk-java-01', '10.30.37.128'),
        ('dwxk-java-00', '10.30.37.90'),
        ('pubService-activeCacheWeb-java-00', '10.30.27.130'),
        ('pubService-activeCacheWeb-java-01', '10.30.27.146'),
        ('pubService-activeCacheWeb-java-02', '10.30.27.32'),
        ('pubService-activeCacheWeb-java-00-tomcat', '10.30.27.130'),
        ('pubService-activeCacheWeb-java-01-tomcat', '10.30.27.146'),
        ('pubService-activeCacheWeb-java-02-tomcat', '10.30.27.32'),
        ('coupon-couponUserWeb-00-tomcat', '10.30.27.247'),
        ('coupon-couponUserWeb-00-dubbo', '10.30.27.247'),
        ('coupon-couponUserWeb-01-tomcat', '10.30.27.116'),
        ('coupon-couponUserWeb-01-dubbo', '10.30.27.116'),
        ('coupon-couponUserWeb-02-tomcat', '10.30.27.152'),
        ('coupon-couponUserWeb-02-dubbo', '10.30.27.152'),
    ]
    for m in jvm_host_list:
        # host,port,vir_port,role,type,node_id
        ipaddr = str(m[1])
        hostname = str(m[0])

        host = "%(port)s.jvm" % {'port': hostname
                                 }

        NEW_HOSTS[host] = {'host': host,
                           'ipaddr': ipaddr,
                           'groupids': [{"groupid": "66"}],
                           'templateidlist': [
                               {'templateid': ZBX_TEMPLATE[u'tcp_status']['id']}
                           ]
                           }
    return NEW_HOSTS


# @logged
def set_autoscaling_list():
    autoscaling_host_list = os.popen(
        "aws cloudwatch list-metrics --namespace 'AWS/AutoScaling' --metric-name GroupDesiredCapacity | grep 'AutoScalingGroupName' | awk '{print $NF}'")
    for m in autoscaling_host_list:
        ipaddr = '10.30.30.31'
        hostname = m.strip()

        host = "%(port)s.autoscaling" % {'port': hostname
                                         }

        NEW_HOSTS[host] = {'host': host,
                           'ipaddr': ipaddr,
                           'groupids': [{"groupid": "70"}],
                           'templateidlist': [
                               {'templateid': ZBX_TEMPLATE[u'AWS Autoscaling template']['id']}
                           ]
                           }
    return NEW_HOSTS


# @logged
def set_ec2_list():
    ec = ec2()
    ec2hosts = ec.getHostInfoList()

    # for host, ipaddr in ec2hosts.items():
    for e in ec2hosts:
        host = e['Name']
        eid = e['eid']
        ipaddr = e['ip']
        instance_type = e['instancetype']

        if instance_type in net_type.keys():
            instance_type_num = net_type[instance_type] * 0.8
            instance_type_num_MB = '%sM' % (instance_type_num,)
        else:
            instance_type_num_MB = '%sM' % 80

        NEW_HOSTS[host] = {'host': host,
                           'ipaddr': ipaddr,
                           'groupids': getHostGid(ipaddr, host),
                           'templateidlist': [
                               {'templateid': ZBX_TEMPLATE[u'Template OS Linux']['id']},
                               {'templateid': ZBX_TEMPLATE[u'tcp_status']['id']},
                               {'templateid': ZBX_TEMPLATE[u'Template ICMP Ping']['id']}
                           ],
                           'macros': [
                               {"macro": "{$EC2_INSTANCE_ID}",
                                "value": eid
                                },
                               {"macro": "{$EC2_INSTANCE_NET_TYPE}",
                                "value": instance_type_num_MB
                                },
                           ]
                           }
    return NEW_HOSTS


# @logged
def set_elb_list():
    e = elb()
    elist = e.getElbTag()
    for e in elist:
        host = e + ".elb"
        if e == 'ads':
            NEW_HOSTS[host] = {'host': host,
                               'ipaddr': '10.30.30.31',
                               'groupids': [{"groupid": "29"}],
                               'templateidlist': [
                                   {'templateid': ZBX_TEMPLATE[u'AWS ELB template for ADS']['id']},
                               ]
                               }
        else:
            NEW_HOSTS[host] = {'host': host,
                               'ipaddr': '10.30.30.31',
                               'groupids': [{"groupid": "29"}],
                               'templateidlist': [
                                   {'templateid': ZBX_TEMPLATE[u'AWS ELB template two']['id']},
                               ]
                               }
    return NEW_HOSTS


# @logged
def add_host_to_zbx():
    for zbx_host, hostinfo in NEW_HOSTS.items():
        if zbx_host not in ZBX_HOSTS.keys():
            zbx.createhost(**hostinfo)
    return 'add host'


# @logged
def del_host_from_zbx():
    for zbx_host in ZBX_HOSTS.keys():
        if zbx_host not in NEW_HOSTS.keys():
            print 'delete ' + zbx_host
            zbx.delhost(zbx_host)
            # 删除 服务器域名解析
            # del_server_domainName(zbx_host, ZBX_HOSTS[zbx_host]['ipaddr'])
    return 'del host'


# @logged
def enable_hosts_to_zbx():
    # ec2_list = []
    host_data = []
    fh = open('ec2_real_list.txt')
    ec = ec2()
    ec2hosts = ec.getHostInfoList()
    for host_list in fh.readlines():
        host_info = host_list.strip()
        host_data.append(host_info)
    for ec2_host in ec2hosts:
        # ec2_list.append(ec2_host['Name'])
        ec2_list = ec2_host['Name']
        if ec2_list not in host_data:
            zbx.enablehost(ec2_list)
    return 'enable ec2_list'


# @logged
def addhost_to_ec2_real_list():
    ec = ec2()
    ec2hosts = ec.getHostInfoList()
    output = open('ec2_real_list.txt', 'w+')
    for e in ec2hosts:
        host = e['Name'] + "\n"
        file_object = output.write(host)
    output.close()


def main():
    set_zbx_hosts()
    set_zbx_template()
    # set_ec2_list()
    # set_elb_list()
    set_mysql_list()
    set_redis_list()
    set_memcache_list()
    # set_jvm_list()
    set_autoscaling_list()
    add_host_to_zbx()

    # enable_hosts_to_zbx()
    # del_host_from_zbx()
    # addhost_to_ec2_real_list()
    # ec = ec2()
    # ec2hosts = ec.getHostInfoList()
    # output =  open('ec2_real_list.txt','w+')
    # for e in ec2hosts:
    #     host =  e['Name']+"\n"
    #     file_object = output.write(host)
    # output.close()


if __name__ == '__main__':
    # updateMacros()
    main()
# print u'10.30.255.57'.encode('utf8')
# del_server_domainName('vpn-bj-01', u'10.30.255.57')
