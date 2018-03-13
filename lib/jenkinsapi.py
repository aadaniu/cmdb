# -*- coding: utf-8 -*-
# 2017-12-20
# by why

import jenkins
import time

from load_config import jenkins_url, jenkins_user_id, jenkins_api_token

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


def get_job_xml(job_name):
    """
        获取job的配置文件
    :param job_name:
    :return:
    """
    return server.get_job_config(job_name)



def create_job_xml(job_name):
    """
        创建固定配置xml
    :param job_name:
    :return:
    """
    base_xml = """
    <?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.plugins.buildblocker.BuildBlockerProperty plugin="build-blocker-plugin@1.7.3">
      <useBuildBlocker>true</useBuildBlocker>
      <blockLevel>UNDEFINED</blockLevel>
      <scanQueueFor>DISABLED</scanQueueFor>
      <blockingJobs>shop-stage-deploy</blockingJobs>
    </hudson.plugins.buildblocker.BuildBlockerProperty>
    <com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty plugin="gitlab-plugin@1.5.2">
      <gitLabConnection>http://git.culiu.org</gitLabConnection>
    </com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty>
    <jenkins.model.BuildDiscarderProperty>
      <strategy class="hudson.tasks.LogRotator">
        <daysToKeep>15</daysToKeep>
        <numToKeep>-1</numToKeep>
        <artifactDaysToKeep>-1</artifactDaysToKeep>
        <artifactNumToKeep>-1</artifactNumToKeep>
      </strategy>
    </jenkins.model.BuildDiscarderProperty>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>REVISION</name>
          <description>git 版本号</description>
          <defaultValue>NULL</defaultValue>
          <trim>false</trim>
        </hudson.model.StringParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <scm class="org.jenkinsci.plugins.multiplescms.MultiSCM" plugin="multiple-scms@0.6">
    <scms>
      <hudson.plugins.git.GitSCM plugin="git@3.6.4">
        <configVersion>2</configVersion>
        <userRemoteConfigs>
          <hudson.plugins.git.UserRemoteConfig>
            <url>git@git.culiu.org:shop/shop.git</url>
            <credentialsId>659fab0e-6f90-484a-a31b-d76fe61899f5</credentialsId>
          </hudson.plugins.git.UserRemoteConfig>
        </userRemoteConfigs>
        <branches>
          <hudson.plugins.git.BranchSpec>
            <name>*/master</name>
          </hudson.plugins.git.BranchSpec>
        </branches>
        <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
        <submoduleCfg class="list"/>
        <extensions>
          <hudson.plugins.git.extensions.impl.RelativeTargetDirectory>
            <relativeTargetDir>shop</relativeTargetDir>
          </hudson.plugins.git.extensions.impl.RelativeTargetDirectory>
        </extensions>
      </hudson.plugins.git.GitSCM>
    </scms>
  </scm>
  <assignedNode>deploy-001</assignedNode>
  <canRoam>false</canRoam>
  <disabled>true</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>true</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>#!/bin/bash -x
. $JENKINS_HOME/tools/lib.sh

echo $GIT_BRANCH

prepare_repo $REVISION shop

#deploy  to master dir

#fab -Htengine-php-A-051 shop.deploy:master,shop,master
echo &quot;------------$(date +&apos;%Y-%m-%d:%H:%M:%S&apos;)------------&quot;
#fab -H &apos;tengine-shop-A-009,tengine-shop-A-010,tengine-shop-A-011,tengine-shop-A-012,tengine-shop-A-013,tengine-shop-A-014,tengine-shop-A-015,tengine-shop-A-016,tengine-shop-A-017,tengine-shop-A-018&apos; -P -z 15 shop.new_dep
loy:master,shop,master
fab -R shop-tengine,dacu-shop-php-fpm,shop-php-fpm -P -z 15 shop.new_deploy:master,shop,master
#fab -R dacu-bg_task shop.new_deploy:master,shop,master
#fab -H tengine-php-product-A-002,tengine-php-wx-A-009,tengine-php-passport-A-003 shop.new_deploy:master,shop,master
#fab -H tengine-php-product-A-002,tengine-php-wx-A-009,tengine-php-passport-A-003,tengine-php-order-A-005 shop.new_deploy:master,shop,master
#fab -H tengine-php-product-A-005  shop.deploy:master,shop,master
#fab -H tengine-php-cart-A-000,tengine-php-cart-A-001,tengine-php-cart-A-002,tengine-php-cart-A-003,tengine-php-cart-A-004,tengine-php-cart-A-005 shop.deploy:master,shop,master
echo &quot;------------$(date +&apos;%Y-%m-%d:%H:%M:%S&apos;)------------&quot;
#fab -R dacu-shop-php-fpm  shop.deploy:master,shop,master
#fab -R shop-seller -P -z3 shop.deploy:master,shop,master

#check Runtime dir
#fab -Rshop-tengine,shop-php-fpm,shop -x shop-018 -P -z5 shop.checkRuntimeDir

# replace with production url
#grep -Rl &apos;wx-dev.chuchujie.com&apos; ${WORKSPACE}/shop/Public/ | xargs sed -i &apos;s/wx-dev.chuchujie.com/wx.chuchujie.com/g&apos; || true

# for qiniu cdn
#cp /home/ec2-user/monkey/conf/qiniu_conf.json qiniu_conf.json.local
#sed -i &quot;s#LOCAL_PUBLIC_DIR#${WORKSPACE}/shop/Public/#&quot; qiniu_conf.json.local
#qrsync qiniu_conf.json.local

# for qcloud cdn
#work_copy=$SVN_WORK_COPY_ROOT/qcloud_cdn_shop
#if [ ! -e $work_copy ];then
#    svn co https://cdn.yun.qq.com/1251001080/shop $work_copy
#fi
#cd $work_copy &amp;&amp; {
#    svn revert -R .
#    rsync -avrl --delete --exclude=&apos;.git&apos; --exclude=&apos;.svn*&apos; $WORKSPACE/shop/Public .
#
#    svn st | grep &apos;!&apos; | awk &apos;{print $NF}&apos; | xargs svn rm --force
#    svn st | grep &apos;?&apos; | awk &apos;{print $NF}&apos; | xargs svn add
#    svn ci -m &apos;update from jenkins&apos;
#}</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers>
    <hudson.plugins.ansicolor.AnsiColorBuildWrapper plugin="ansicolor@0.5.2">
      <colorMapName>xterm</colorMapName>
    </hudson.plugins.ansicolor.AnsiColorBuildWrapper>
  </buildWrappers>
</project>
Traceback (most recent call last):
  File "lib/jenkinsapi.py", line 52, in <module>
    f.write(job_xml)
UnicodeEncodeError: 'ascii' codec can't encode characters in position 1230-1232: ordinal not in range(128)

F:\whyscmdb\whyscmdb>python lib/jenkinsapi.py
<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties>
    <hudson.plugins.buildblocker.BuildBlockerProperty plugin="build-blocker-plugin@1.7.3">
      <useBuildBlocker>true</useBuildBlocker>
      <blockLevel>UNDEFINED</blockLevel>
      <scanQueueFor>DISABLED</scanQueueFor>
      <blockingJobs>shop-stage-deploy</blockingJobs>
    </hudson.plugins.buildblocker.BuildBlockerProperty>
    <com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty plugin="gitlab-plugin@1.5.2">
      <gitLabConnection>http://git.culiu.org</gitLabConnection>
    </com.dabsquared.gitlabjenkins.connection.GitLabConnectionProperty>
    <jenkins.model.BuildDiscarderProperty>
      <strategy class="hudson.tasks.LogRotator">
        <daysToKeep>15</daysToKeep>
        <numToKeep>-1</numToKeep>
        <artifactDaysToKeep>-1</artifactDaysToKeep>
        <artifactNumToKeep>-1</artifactNumToKeep>
      </strategy>
    </jenkins.model.BuildDiscarderProperty>
    <hudson.model.ParametersDefinitionProperty>
      <parameterDefinitions>
        <hudson.model.StringParameterDefinition>
          <name>REVISION</name>
          <description>git 版本号</description>
          <defaultValue>NULL</defaultValue>
          <trim>false</trim>
        </hudson.model.StringParameterDefinition>
      </parameterDefinitions>
    </hudson.model.ParametersDefinitionProperty>
  </properties>
  <scm class="org.jenkinsci.plugins.multiplescms.MultiSCM" plugin="multiple-scms@0.6">
    <scms>
      <hudson.plugins.git.GitSCM plugin="git@3.6.4">
        <configVersion>2</configVersion>
        <userRemoteConfigs>
          <hudson.plugins.git.UserRemoteConfig>
            <url>git@git.culiu.org:shop/shop.git</url>
            <credentialsId>659fab0e-6f90-484a-a31b-d76fe61899f5</credentialsId>
          </hudson.plugins.git.UserRemoteConfig>
        </userRemoteConfigs>
        <branches>
          <hudson.plugins.git.BranchSpec>
            <name>*/master</name>
          </hudson.plugins.git.BranchSpec>
        </branches>
        <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
        <submoduleCfg class="list"/>
        <extensions>
          <hudson.plugins.git.extensions.impl.RelativeTargetDirectory>
            <relativeTargetDir>shop</relativeTargetDir>
          </hudson.plugins.git.extensions.impl.RelativeTargetDirectory>
        </extensions>
      </hudson.plugins.git.GitSCM>
    </scms>
  </scm>
  <assignedNode>deploy-001</assignedNode>
  <canRoam>false</canRoam>
  <disabled>true</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>true</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>#!/bin/bash -x
. $JENKINS_HOME/tools/lib.sh

echo $GIT_BRANCH

prepare_repo $REVISION shop

#deploy  to master dir

#fab -Htengine-php-A-051 shop.deploy:master,shop,master
echo &quot;------------$(date +&apos;%Y-%m-%d:%H:%M:%S&apos;)------------&quot;
#fab -H &apos;tengine-shop-A-009,tengine-shop-A-010,tengine-shop-A-011,tengine-shop-A-012,tengine-shop-A-013,tengine-shop-A-014,tengine-shop-A-015,tengine-shop-A-016,tengine-shop-A-017,tengine-shop-A-018&apos; -P -z 15 shop.new_dep
loy:master,shop,master
fab -R shop-tengine,dacu-shop-php-fpm,shop-php-fpm -P -z 15 shop.new_deploy:master,shop,master
#fab -R dacu-bg_task shop.new_deploy:master,shop,master
#fab -H tengine-php-product-A-002,tengine-php-wx-A-009,tengine-php-passport-A-003 shop.new_deploy:master,shop,master
#fab -H tengine-php-product-A-002,tengine-php-wx-A-009,tengine-php-passport-A-003,tengine-php-order-A-005 shop.new_deploy:master,shop,master
#fab -H tengine-php-product-A-005  shop.deploy:master,shop,master
#fab -H tengine-php-cart-A-000,tengine-php-cart-A-001,tengine-php-cart-A-002,tengine-php-cart-A-003,tengine-php-cart-A-004,tengine-php-cart-A-005 shop.deploy:master,shop,master
echo &quot;------------$(date +&apos;%Y-%m-%d:%H:%M:%S&apos;)------------&quot;
#fab -R dacu-shop-php-fpm  shop.deploy:master,shop,master
#fab -R shop-seller -P -z3 shop.deploy:master,shop,master

#check Runtime dir
#fab -Rshop-tengine,shop-php-fpm,shop -x shop-018 -P -z5 shop.checkRuntimeDir

# replace with production url
#grep -Rl &apos;wx-dev.chuchujie.com&apos; ${WORKSPACE}/shop/Public/ | xargs sed -i &apos;s/wx-dev.chuchujie.com/wx.chuchujie.com/g&apos; || true

# for qiniu cdn
#cp /home/ec2-user/monkey/conf/qiniu_conf.json qiniu_conf.json.local
#sed -i &quot;s#LOCAL_PUBLIC_DIR#${WORKSPACE}/shop/Public/#&quot; qiniu_conf.json.local
#qrsync qiniu_conf.json.local

# for qcloud cdn
#work_copy=$SVN_WORK_COPY_ROOT/qcloud_cdn_shop
#if [ ! -e $work_copy ];then
#    svn co https://cdn.yun.qq.com/1251001080/shop $work_copy
#fi
#cd $work_copy &amp;&amp; {
#    svn revert -R .
#    rsync -avrl --delete --exclude=&apos;.git&apos; --exclude=&apos;.svn*&apos; $WORKSPACE/shop/Public .
#
#    svn st | grep &apos;!&apos; | awk &apos;{print $NF}&apos; | xargs svn rm --force
#    svn st | grep &apos;?&apos; | awk &apos;{print $NF}&apos; | xargs svn add
#    svn ci -m &apos;update from jenkins&apos;
#}</command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers>
    <hudson.plugins.ansicolor.AnsiColorBuildWrapper plugin="ansicolor@0.5.2">
      <colorMapName>xterm</colorMapName>
    </hudson.plugins.ansicolor.AnsiColorBuildWrapper>
  </buildWrappers>
</project>
    """

    return 0




if __name__ == "__main__":
    job_xml = get_job_xml('shop-master-deploy')
    print job_xml
    with open('a.xml', 'w') as f:
        f.write(job_xml)
