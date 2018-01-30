# cmdb

## 介绍

由于就职电商平台，业务复杂，需要一套完善的基础设置来减少日常运维中重复工作和业务方咨询或者部署方面需要编写的cmdb。

本cmdb基于salt(与fab同时使用)，zabbix，标准化的机器名，业务部署路径，目录结构，部署路径，云厂商api等完成自动化运维。

部门，业务线进而对于所有资源(domain,lb，host)进行标记，主机区分为nginx，nginx+php-fpm，php-fpm，mysql，redis，memcache，op等，规范db，业务部署路径，日志结构等。

- 报警维度为运维部分业务线维度，op和db维度，业务部只区分业务线维度；
- jenkins名称规范，部门_业务线_代码仓库_环境（dev，pro，long），pro部署权限交付给业务线负责人，其他环境所有人都有，然后根据需要进行jenkins权限修改
- git权限根据业务自行修改即可
- salt和fab主机组根据部门-业务线（-可选功能或备注），默认根据部门-业务线自动生成，可添加自定义任务组


### 资源自动添加到业务线
1. 控制台添加主机，通过标签添加到对应业务线，或者通过名称区分业务线
2. 控制台添加lb，通过标签添加业务线，
3. cmdb域名，封装好，添加业务线
4. 业务线创建环境，通过选择域名记录，通过salt来创建初步环境
5. 通过控制台创建的通过cmdb定时任务定时拉数据
6. 通过cmdb创建自动创建并添加到业务线

## cmdb功能

### 工单workorder

### 管理功能opmanage

#### index
1. 登录
2. 退出
3. 验证登录装饰器
4. 验证权限装饰器

#### user
1. 添加用户->添加到cmdb->创建zabbix用户等等一系列用户(->发送邮件用户)?
2. 删除用户->从cmdb删除->删除zabbix用户等等一系列用户
3. 用户自助修改密码？
4. 修改用户信息->修改cmdb->更新用户？
5. 查询指定用户信息
6. 获取所有用户信息

#### domain
1. 创建域名->添加域名解析？->添加到cmdb
2. 删除域名->删除域名解析？->从cmdb删除
3. 修改域名->修改域名解析？一般都是修改记录的后端值

#### lb
1. 创建负载->添加到cmdb->添加负载监控
2. 删除负载->从cmdb删除->删除负载监控
3. 获取负载信息？

#### host
1. 创建主机->添加到cmdb->添加主机监控->根据主机信息添加模板
2. 删除主机->从cmdb删除->删除主机监控
3. 更新主机名->更新主机
4. 启动主机/关停主机->开启/关闭主机监控
5. 根据报警启动/关闭主机监控?
6. 获取主机信息？

#### dep
1. 创建业务线
2. 删除业务线->业务线下资源(理论上资源是先走的)

#### db
不负责db相关，不了解

### 运维自动化salt

主机组管理
主机组
salt执行

### 安全相关waf

通过salt远程部署waf配置文件
自助服务砍量
机器开放端口扫描？如何实现(定时任务)

### 报警信息自助分析op*****
实现思路，业务报警，自动分析可能出现这个报警的原因，然后获取相关指标展示

### 日志diskclean
清理
上传

### 汇总展示dashboard

1. 报警总数，信息汇总
2. 资产统计
3. 业务时间线
4. aws账单


## 依赖包
- djang (1.11.5)
- pymysql (0.7.11)
- boto3 (1.4.8)
- qcloudapi-sdk-python (2.0.10)
- aliyun-python-sdk-core (2.6.0)
- aliyun-python-sdk-ecs (4.4.3)
- python-jenkins (0.4.15)
- apscheduler (3.5.0)


## 配置文件
- global.config 用于公司全局配置
- cmdb.config   cmdb依赖配置
- zabbix.config zabbix依赖配置
- jenkins.config  jenkins配置

## 生成数据库并启动服务

- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

## 数据初始化

```
python manage.py shell

from opmanage.models import  *
Department_info.objects.create(department_name='op',department_leader='opleader',department_email='op@whysdomain.com')
User_info.objects.create(username='cmdbadmin',password='123456',email='why@whysdomain.com',auth='1',jumper='f',vpn='f',phone='13552493019', department_id = 1, git= 'f',zabbix='f',jenkins='f')
Serverline_info.objects.create(serverline_name='op-basic-cmdb',serverline_leader='wanghongyu',serverline_op_leader='wanghongyu',department_id='1')
Show_info.objects.create(username_id=1)
```

## 坑

酷狗音乐会占用8000端口，导致django使用默认端口起不来，报错为 `Error: [Errno 10013]`

