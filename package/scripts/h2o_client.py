# -*- coding: utf-8 -*--
from resource_management import *


class Client(Script):
    def install(self, env):
        Logger.info("安装开始")
        Logger.info("安装结束")

    def configure(self, env):
        Logger.info("配置开始")
        Logger.info("配置结束")

    def status(self, env):
        Logger.info("检查状态开始")
        raise ClientComponentHasNoStatus()
        Logger.info("检查状态结束")


if __name__ == "__main__":
    Client().execute()
