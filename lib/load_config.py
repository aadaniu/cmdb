# -*- coding: utf-8 -*-
# 2017-11-29
# by why

import os
import sys
import ConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print os.path.join(BASE_DIR, 'config\cmdb.config')

# load cmdb config

cmdb_config = ConfigParser.RawConfigParser()
cmdb_config.read(os.path.join(BASE_DIR, 'config\cmdb.config'))

cmdb_mysql_host = cmdb_config.get('mysql','host')
cmdb_mysql_port = cmdb_config.get('mysql','port')
cmdb_mysql_user = cmdb_config.get('mysql','user')
cmdb_mysql_password = cmdb_config.get('mysql','password')
cmdb_mysql_database = cmdb_config.get('mysql','database')

# load zabbix config

zabbix_config = ConfigParser.RawConfigParser()
zabbix_config.read(os.path.join(BASE_DIR, 'config/zabbix.config'))

zabbix_api_url = zabbix_config.get('api','url')
zabbix_api_username = zabbix_config.get('api','username')
zabbix_api_passport = zabbix_config.get('api','password')

zabbix_mysql_host = zabbix_config.get('mysql','host')
zabbix_mysql_port = zabbix_config.get('mysql','port')
zabbix_mysql_user = zabbix_config.get('mysql','user')
zabbix_mysql_passport = zabbix_config.get('mysql','password')
zabbix_mysql_database = zabbix_config.get('mysql','database')
