# -*- coding: utf-8 -*-
# 2017-12-10
# by why

from datetime import datetime

__author__ = 'jecy'
import boto3


class ec2(object):
    def __init__(self, istatus=None, **kwargs):
        session = boto3.Session(profile_name="control-center-for-op")
        self.client = session.client('ec2', **kwargs)
        if not istatus:
            istatus = ['running']
        self.ec2dic = {}
        self.istatus = istatus
        self.__getEc2list()
        # self.client = boto3.client('ec2')

    def refresh(self):
        self.__getEc2list()

    def __getEc2list(self, ):

        response = self.client.describe_instances(Filters=[])
        self.ec2dic = response

    def delete_tag(self, eids):
        self.client.delete_tags(
            Resources=eids,
            Tags=[
                {
                    'Key': u'\u540d\u79f0',
                }
            ]
        )

    def getStopedList(self):
        client = boto3.client('ec2')
        response = client.describe_instances(
            Filters=[{'Name': 'instance-state-name',
                      'Values': ['stopped']}, ])
        for r in response['Reservations']:
            for i in r['Instances']:
                if 'Platform' in i.keys():
                    continue
                for tag in i['Tags']:
                    if tag['Key'] == u'\u540d\u79f0':
                        print  tag['Value']
                        continue

    def changeNameTagByTypetag(self, typeTagValue="bd-emr", NameTagHead="bd-slave"):
        serviceMaxTagNum = 0
        noNameHosts = []
        for r in self.ec2dic['Reservations']:
            for i in r['Instances']:
                typetag = None
                hostname = None
                for tag in i['Tags']:
                    if tag['Key'] == u'\u540d\u79f0':
                        hostname = tag['Value']
                        continue
                    if tag['Key'] == u'type':
                        typetag = tag['Value']
                        continue
                if typetag != typeTagValue:
                    continue
                if hostname.startswith(NameTagHead):
                    hostnametagnum = int(hostname.split('-')[-1])
                    serviceMaxTagNum = max(serviceMaxTagNum, hostnametagnum)
                else:
                    Id = i['InstanceId']
                    noNameHosts.append(Id)
        # change Name
        for iid in noNameHosts:
            serviceMaxTagNum += 1
            NameTagBottom = str(serviceMaxTagNum) if serviceMaxTagNum > 9 else "0" + str(serviceMaxTagNum)
            HostName = NameTagHead + '-' + NameTagBottom
            print iid, HostName
            self.__setTag(iid, u'\u540d\u79f0', HostName)

    def getAllHostInfo(self):
        result = []
        response = self.ec2dic
        for r in response['Reservations']:
            for i in r['Instances']:
                if 'Platform' in i.keys():
                    continue
                ip = '127.0.0.1'
                if 'PrivateIpAddress' in i.keys():
                    ip = i['PrivateIpAddress']
                eid = i['InstanceId']
                State = i['State']['Name']
                Name = ccmod_Modules = ccmod_Groups = ''
                if 'Tags' in i.keys():
                    for tag in i['Tags']:
                        if tag['Key'] == u'Name':
                            Name = tag['Value']
                            continue
                        if tag['Key'] == u'ccmod_Modules':
                            ccmod_Modules = tag['Value']
                            continue
                        if tag['Key'] == u'ccmod_Groups':
                            ccmod_Groups = tag['Value']
                            continue
                if Name == '':
                    continue
                zone = i['Placement']['AvailabilityZone']
                result.append({'eid': eid,
                               'ip': ip,
                               'hostname': Name,
                               'zone': zone,
                               'state': State,
                               'ccmod_Modules': ccmod_Modules,
                               'ccmod_Groups': ccmod_Groups
                               })
        return result

    def getHostInfoList(self):
        result = []
        client = boto3.client('ec2')
        response = client.describe_instances(
            Filters=[{'Name': 'instance-state-name',
                      'Values': ['running']}, ])
        for r in response['Reservations']:
            for i in r['Instances']:
                if 'Platform' in i.keys():
                    continue
                ip = i['PrivateIpAddress']
                eid = i['InstanceId']
                InstanceType = i["InstanceType"]
                type = i['InstanceType']
                oldname = ''
                Name = ''
                ServiceLine = None
                for tag in i['Tags']:
                    if tag['Key'] == u'Name':
                        Name = tag['Value']
                        continue
                    if tag["Key"] == u'ServiceLine':
                        ServiceLine = tag['Value']
                        continue
                if Name == '':
                    continue
                LauchTime = i['LaunchTime'].replace(tzinfo=None).strftime('%s')
                NowTime = datetime.utcnow().strftime('%s')

                zone = i['Placement']['AvailabilityZone']
                result.append({'eid': eid,
                               'ip': ip,
                               'hostname': Name,
                               'instancetype': type,
                               'zone': zone,
                               'oldname': oldname,
                               'Name': Name,
                               'StarTime': int(NowTime) - int(LauchTime),
                               })
        return result

    def setOldNameTag(self, eid, oldname):
        self.__setTag(eid, key='oldName', value=oldname)

    def setNameTag(self, eid, name):
        self.__setTag(eid, key='Name', value=name)
        # self.__setTag(eid, key=u'\u540d\u79f0', value=name)

    def __setTag(self, eid, key, value):
        value = str(value)
        client = boto3.client('ec2')
        client.create_tags(
            # DryRun=True,
            Resources=[
                eid,
            ],
            Tags=[
                {
                    'Key': key,
                    'Value': value
                },
            ]
        )

    def getNameHasChanged(self):
        list = {}
        for r in self.ec2dic['Reservations']:
            for i in r['Instances']:
                # print i
                if 'Platform' in i.keys():
                    continue
                ip = i['PrivateIpAddress']
                hostname = None
                oldname = None
                name = None
                for tag in i['Tags']:
                    if tag['Key'] == u'\u540d\u79f0':
                        hostname = tag['Value']
                    elif tag['Key'] == u'oldName':
                        oldname = tag['Value']
                    elif tag['Key'] == u'Name':
                        name = tag['Value']

                if not hostname and not name:
                    continue
                if hostname != name:
                    hostname = hostname if hostname else name
                    eid = i['InstanceId']
                    self.setNameTag(eid, hostname)
                if hostname == oldname:
                    continue
                list[ip] = hostname
        return list

    def getId(self, ip):
        for r in self.ec2dic['Reservations']:
            for i in r['Instances']:
                if i['PrivateIpAddress'] == ip:
                    return i['InstanceId']

    def getIdByHostname(self, hostname=None):
        for r in self.ec2dic['Reservations']:
            for i in r['Instances']:
                if hostname:
                    if "Tags" in i.keys():
                        for tag in i['Tags']:
                            if tag['Value'] == hostname:
                                return i['InstanceId']

    def getInstanceIds(self):
        result = {}
        for r in self.ec2dic['Reservations']:
            for i in r['Instances']:
                if 'Platform' in i.keys():
                    continue
                hostname = None
                if 'Tags' in i.keys():
                    for tag in i['Tags']:
                        if tag['Key'] == u'Name':
                            hostname = tag['Value']
                if hostname:
                    result[i['InstanceId']] = hostname
        return result

    def getTag(self):
        '''

        :return: list:
            {'ip':'hostname'}
        '''
        list = {}
        for r in self.ec2dic['Reservations']:
            for i in r['Instances']:
                if 'Platform' in i.keys():
                    continue
                ip = i['PrivateIpAddress']
                hostname = ''
                for tag in i['Tags']:
                    if tag['Key'] == u'\u540d\u79f0':
                        hostname = tag['Value']
                        break
                if hostname == '':
                    continue
                list[ip] = hostname
        return list

    def getHostIPs(self):
        '''

        :return: list:
            {'name':'ip'}
        '''
        list = {}
        for r in self.ec2dic['Reservations']:
            for i in r['Instances']:
                if 'Platform' in i.keys():
                    continue
                ip = i['PrivateIpAddress']
                hostname = ''
                for tag in i['Tags']:
                    if tag['Key'] == u'\u540d\u79f0':
                        hostname = tag['Value']
                        break
                if hostname == '':
                    continue
                list[hostname] = ip
        return list

    def getHostBeteen(self, star=600, end=70000):
        '''

        :return: dic
                {'hostname':'instance type'}
        '''
        result = {}
        now = datetime.utcnow()

        stoptime = now.strftime('%s')
        for r in self.ec2dic['Reservations']:
            for i in r['Instances']:
                # print i
                if 'Platform' in i.keys():
                    continue
                ip = i['PrivateIpAddress']
                hostname = ''
                for tag in i['Tags']:
                    if tag['Key'] == u'\u540d\u79f0':
                        hostname = tag['Value']
                        break
                if hostname == '':
                    continue
                startime = i['LaunchTime'].replace(tzinfo=None).strftime('%s')
                if star < int(stoptime) - int(startime) < end:
                    result[hostname] = ip
        return result

    def getInstanceType(self):
        '''

        :return: dic
                {'hostname':'instance type'}
        '''
        list = {}
        for r in self.ec2dic['Reservations']:
            for i in r['Instances']:
                # print i

                if 'Platform' in i.keys():
                    continue
                hostname = ''
                if 'Tags' in i.keys():
                    for tag in i['Tags']:
                        if tag['Key'] == u'Name':
                            hostname = tag['Value']
                            break
                if hostname == '':
                    continue
                list[hostname] = i['InstanceType']
        return list

    def getSecurityGroups(self):
        '''

        :return: dic
                {'hostname':'instance type'}
        '''
        list = {}
        for r in self.ec2dic['Reservations']:
            for i in r['Instances']:
                # print i

                if 'Platform' in i.keys():
                    continue
                ip = i['PrivateIpAddress']
                securitygroup = i['SecurityGroups']
                hostname = ''
                for tag in i['Tags']:
                    if tag['Key'] == u'\u540d\u79f0':
                        hostname = tag['Value']
                        break
                if hostname == '':
                    continue
                list[ip] = i['SecurityGroups']
        return list

    def getNewStarts(self, recentime=60, BEFOR=True):
        '''

        :return: dic
                {'hostname':'instance type'}
        '''
        result = []
        now = datetime.utcnow()

        for r in self.ec2dic['Reservations']:
            for i in r['Instances']:
                # print i
                if 'Platform' in i.keys():
                    continue
                ip = i['PrivateIpAddress']
                hostname = ''
                for tag in i['Tags']:
                    if tag['Key'] == u'\u540d\u79f0':
                        hostname = tag['Value']
                        break
                if hostname == '':
                    continue
                # if hostname != 'mysql-db-015':
                #     continue
                startime = i['LaunchTime'].replace(tzinfo=None).strftime('%s')
                stoptime = now.strftime('%s')
                # print (now - i['LaunchTime'].replace(tzinfo=None)).seconds
                if int(stoptime) - int(startime) < recentime and BEFOR:
                    result.append({'InstanceId': i['InstanceId'],
                                   'InstanceName': hostname,
                                   'InstanceIP': ip})
        return result

    def getinfo(self):
        '''

        :return: list:
            {'ip':'hostname'}
        '''
        result = [
            '"服务器名称","操作系统名称及版本","数据库名称及版本","所支持的信息系统名称","信息系统支持的主要业务流程","业务流程的重要程度","当前版本","使用部门","开发方式（完全外包\购买\定制）","业务系统后台维护管理员","操作系统管理员","数据库系统管理员","上线时间","最近一次重要升级时间","服务器所在地"\n']
        for r in self.ec2dic['Reservations']:
            for i in r['Instances']:
                # print i
                if 'Platform' in i.keys():
                    continue
                ip = i['PrivateIpAddress']
                hostname = ''
                for tag in i['Tags']:
                    if tag['Key'] == u'\u540d\u79f0':
                        hostname = tag['Value']
                        break
                if hostname == '':
                    continue
                info = []
                starttime = i['LaunchTime']
                deparment = '数据部' if hostname.startswith('emr') else '技术部'
                businessadmin = '王宇杰' if hostname.startswith('emr') else '李顺'
                infoname = '/'.join(hostname.split('-')[:-1])
                info.append('"%s"' % hostname)
                info.append('"Amazon Linux AMI 2015.03.1 x86_64 HVM GP2"')
                info.append('"无"')  # 数据库版本
                info.append('"%s"' % infoname)  # 所支持的系统名称
                info.append('"%s"' % infoname)  # 信息系统致辞的主要业务流程
                info.append('"重要"')  # 业务流程的重要程度
                info.append('"无"')  # 当前版本
                info.append('"%s"' % deparment)  # 使用部门
                info.append('"定制"')  # 开发方式（完全外包\购买\定制）
                info.append('"%s"' % businessadmin)  # 业务系统后台维护管理员
                info.append('"无"')  # 操作系统管理员
                info.append('"林建星、郭颂"')  # 数据库管理员
                info.append('"%s"' % starttime)  # 上线时间
                info.append('"无"')  # 最近一次重要升级时间
                info.append('"亚马逊虚拟化平台"')  # 服务器所在地
                # print info
                result.append(','.join(info))
        return result


if __name__ == '__main__':
    ee = ec2()

    # for xx in e.getHostInfoList():
    #     print xx
    # e = ec2(istatus=['stopped', 'running'])
    # print e.ec2dic
    # print e.getNewStarts(recentime=120)
    # print e.getNewStarts(recentime=10000)

    # with open('/tmp/txt.csv', 'w') as t:
    #     for h in e.getinfo():
    #         t.write('%s\n' % h)
    pass
