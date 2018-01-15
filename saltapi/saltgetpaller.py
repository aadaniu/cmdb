# -*- coding: utf-8 -*-
# 2018-01-15
# by why

import urllib2
import json


def ext_pillar(minion_id, pillar, *args, **kwargs):
    try:
        ip = minion_id.split('-')[-1]
        url = 'http://xxx.xxx.com/public/api/SaltPillarInfo/{ip}/'.format(ip=ip)
        request = urllib2.urlopen(url=url, timeout=30)
        response = request.read()
        data = json.loads(response)
    except Exception as e:
        data = {}

    return {'gameInfo': data}