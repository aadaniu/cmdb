# -*- coding: utf-8 -*-
# 2017-12-10
# by why

from tmp.ec2 import ec2

__author__ = 'jecy'
import boto3

ee = ec2()
session = boto3.Session(profile_name="control-center-for-op")
client = session.client('elb')


class elb:
    def __init__(self):
        self.elbdic = {}
        self.elbname = None
        self.__getElblist()
        self.instancelist = []
        self.ec2idilist = ee.getInstanceIds()
        # self.client = boto3.client('ec2')

    def refresh(self):
        self.__getElblist()
        return

    def __getElblist(self):
        self.elbdic = client.describe_load_balancers()
        return self.elbdic

    def getElbTag(self):
        result = []
        for e in self.elbdic['LoadBalancerDescriptions']:
            result.append(e['LoadBalancerName'])
        return result

    def setElbName(self, name):
        self.elbname = name
        self.__setInstanceList()
        return self.elbname

    def __setInstanceList(self):
        self.__getElblist()
        self.instancelist = []
        for e in self.elbdic['LoadBalancerDescriptions']:
            if e['LoadBalancerName'] == self.elbname:
                for i in e['Instances']:
                    self.instancelist.append(self.ec2idilist[i['InstanceId']])
        return self.instancelist

    def instanceIsInService(self, instance):
        if not self.isInstance(instance):
            return False
        instanceid = ee.getIdByHostname(instance)
        response = client.describe_instance_health(
            LoadBalancerName=self.elbname,
            Instances=[
                {
                    'InstanceId': instanceid
                }
            ]
        )
        return response['InstanceStates'][0]['State'] == 'InService'

    def addInstance(self, instance):
        instanceid = ee.getIdByHostname(instance)
        client.register_instances_with_load_balancer(
            LoadBalancerName=self.elbname,
            Instances=[
                {
                    'InstanceId': instanceid,
                }
            ]
        )
        return 'add instance %s ' % instance

    def removeInstance(self, instance):
        instanceid = ee.getIdByHostname(instance)
        client.deregister_instances_from_load_balancer(
            LoadBalancerName=self.elbname,
            Instances=[
                {
                    'InstanceId': instanceid,
                }
            ]

        )
        return 'remove instance %s' % instance

    def isInstance(self, instance=None):
        self.__setInstanceList()
        return instance in self.instancelist


if __name__ == '__main__':
    e = elb()
    print e.elbdic
