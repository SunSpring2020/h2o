# -*- coding: utf-8 -*-
# !/usr/bin/env python
import json
from resource_management import *

config = Script.get_config()

# 组件下载地址
h2o_download_url = 'http://fileserver.cn/HDP/centos6.5/h2o/h2o-3.32.1.7.tar.gz'
if bool(config.get('hostLevelParams')) & bool(config['hostLevelParams'].get("repo_info")):
    baseUrl = json.loads(config['hostLevelParams']['repo_info'])[0]['baseUrl']
    h2o_download_url = format("{baseUrl}/h2o/h2o-3.32.1.7.tar.gz")

# h2o env
h2o_user = config['configurations']['h2o-env']['h2o.user']
h2o_group = config['configurations']['h2o-env']['h2o.group']
# h2o安装目录
h2o_base_dir = '/usr/hdp/2.5.3.0-37/h2o'
# h2o 日志目录
h2o_log_dir = config['configurations']['h2o-env']['env.log.dir']
# h2o pid目录
h2o_pid_dir = config['configurations']['h2o-env']['env.pid.dir']
# h2o pid文件
h2o_pid_file = format('{h2o_pid_dir}/h2o.pid')

# h2o config
# h2o节点总堆大小
heap_size_num = default("/configurations/h2o-config/heap.size", 1)
heap_size = format('{heap_size_num}g')
# h2o集群名称
cluster_name = config['configurations']['h2o-config']['cluster.name']
# Web的运行时监视器端口
rest_port = config['configurations']['h2o-config']['rest.port']
# flow保存地址
flow_dir = config['configurations']['h2o-config']['flow.dir']

if bool(config.get('hostLevelParams')) & bool(config['hostLevelParams'].get("java_home")):
    java_home = config['hostLevelParams']['java_home']
