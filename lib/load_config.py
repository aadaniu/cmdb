# -*- coding: utf-8 -*-
# 2017-11-29
# by why

import os
import sys
import ConfigParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# load cmdb config

cmdb_config = ConfigParser.RawConfigParser()
cmdb_config.read(os.path.join(BASE_DIR, 'config/cmdb.config'))

cmdb_mysql_host = cmdb_config.get('mysql','host')
cmdb_mysql_port = cmdb_config.get('mysql','port')
cmdb_mysql_user = cmdb_config.get('mysql','user')
cmdb_mysql_password = cmdb_config.get('mysql','password')
cmdb_mysql_database = cmdb_config.get('mysql','database')

cmdb_smtp_host = cmdb_config.get('smtp','host')
cmdb_smtp_port = cmdb_config.get('smtp','port')
cmdb_smtp_user = cmdb_config.get('smtp','user')
cmdb_smtp_password = cmdb_config.get('smtp','password')


# load zabbix config

zabbix_config = ConfigParser.RawConfigParser()
zabbix_config.read(os.path.join(BASE_DIR, 'config/zabbix.config'))

zabbix_api_host = zabbix_config.get('api','host')
zabbix_api_url = zabbix_config.get('api','url')
zabbix_api_username = zabbix_config.get('api','username')
zabbix_api_password = zabbix_config.get('api','password')

zabbix_mysql_host = zabbix_config.get('mysql','host')
zabbix_mysql_port = zabbix_config.get('mysql','port')
zabbix_mysql_user = zabbix_config.get('mysql','user')
zabbix_mysql_password = zabbix_config.get('mysql','password')
zabbix_mysql_database = zabbix_config.get('mysql','database')

# load global config

global_config = ConfigParser.RawConfigParser()
global_config.read(os.path.join(BASE_DIR, 'config/global.config'))

global_all_email_suffix = global_config.get('all','email_suffix')

# load jenkins config

jenkins_config = ConfigParser.RawConfigParser()
jenkins_config.read(os.path.join(BASE_DIR, 'config/jenkins.config'))

jenkins_url = jenkins_config.get('jenkins','url')
jenkins_user_id = jenkins_config.get('jenkins','user_id')
jenkins_api_token = jenkins_config.get('jenkins','api_token')


