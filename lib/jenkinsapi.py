# -*- coding: utf-8 -*-
# 2017-12-20
# by why

import jenkins
import time

from lib.load_config import jenkins_url, jenkins_user_id, jenkins_api_token

server = jenkins.Jenkins(jenkins_url, username=jenkins_user_id, password=jenkins_api_token)

def getLastThreeBuildTimes(job_name):
    """
        获取最后三次构建的时间
    :param job_name:
    :return:
    """
    last_build_num = server.get_job_info(job_name)['lastBuild']['number']
    num = int(last_build_num)
    last_three_build_times = []
    for i in [num, num - 1, num - 2]:
        try:
            # 不知道为什么获取的时候莫名其妙的多了三个0
            build_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(server.get_build_info(job_name, i)['timestamp']/1000))
            # server.get_build_console_output(job_name, i)
            last_three_build_times.append(build_time)
        except:
            pass

    return last_three_build_times



# jenkins权限都在config.xml文件中。