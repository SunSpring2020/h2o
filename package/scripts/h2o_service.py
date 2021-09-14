# -*- coding: utf-8 -*-

import os, json
from resource_management import *


class H2oService(Script):

    def install(self, env):
        Logger.info("安装开始")
        import params
        env.set_params(params)

        # 创建目录
        Directory([params.h2o_base_dir, params.h2o_log_dir, params.h2o_pid_dir, params.flow_dir],
                  mode=0755,
                  cd_access='a',
                  create_parents=True,
                  owner=params.h2o_user,
                  group=params.h2o_group)

        # 下载h2o安装包
        cmd = format("cd {h2o_base_dir}; wget {h2o_download_url} -O h2o.tar.gz")
        Execute(cmd, user=params.h2o_user)

        # 解压h2o安装包
        cmd = format("cd {h2o_base_dir}; tar -zxvf h2o.tar.gz")
        Execute(cmd, user=params.h2o_user)

        # 移除h2o安装包
        cmd = format("cd {h2o_base_dir}; rm -rf h2o.tar.gz")
        Execute(cmd, user=params.h2o_user)

        Logger.info("安装结束")

    def configure(self, env):
        Logger.info("配置开始")
        import params
        env.set_params(params)

        Logger.info("配置结束")

    def start(self, env):
        Logger.info("启动开始")
        import params
        env.set_params(params)

        # 配置h2o
        self.configure(env)

        Execute("source /etc/profile", user=params.h2o_user)
        # 启动h2o
        cmd = format(
            "nohup {java_home}/bin/java -Xmx{heap_size} -jar {h2o_base_dir}/h2o.jar -name {cluster_name} -port {rest_port} -log_dir {h2o_log_dir} -flow_dir {flow_dir} &")
        Execute(cmd, user=params.h2o_user)

        # 保存进程id
        Execute("ps -ef | grep h2o.jar | grep -v grep | awk '{print $2}' > " + params.h2o_pid_file,
                user=params.h2o_user)

        Logger.info("启动结束")

    def stop(self, env):
        Logger.info("停止开始")
        import params
        env.set_params(params)

        pid_file = params.h2o_pid_file
        pid = os.popen('cat {pid_file}'.format(pid_file=pid_file)).read()

        process_id_exists_command = format("ls {pid_file} && ps -p {pid}")

        kill_cmd = format("kill {pid}")
        Execute(kill_cmd, not_if=format("! ({process_id_exists_command})"), user=params.h2o_user)
        wait_time = 5

        hard_kill_cmd = format("kill -9 {pid}")
        Execute(hard_kill_cmd, not_if=format(
            "! ({process_id_exists_command}) || ( sleep {wait_time} && ! ({process_id_exists_command}) )"),
                ignore_failures=True, user=params.h2o_user)

        File(pid_file, action="delete")

        Logger.info("停止成功")

    def status(self, env):
        Logger.info("查看状态开始")
        import params
        env.set_params(params)

        # 根据pid检查文件状态
        check_process_status(params.h2o_pid_file)
        Logger.info("查看状态结束")

    def restart(self, env):
        Logger.info("重启开始")
        self.stop(env)
        self.start(env)
        Logger.info("重启成功")


if __name__ == "__main__":
    H2oService().execute()
