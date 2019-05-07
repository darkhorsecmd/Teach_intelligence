# -*- coding: utf-8 -*-
# @Time    : 2019/4/7 21:29
# @Author  : 郭增祥
# @File    : Mylog-教师信息挖掘
from logzero import logger
import logzero
import logging
import os
import uuid
#!!!!!!!!!!!!!!!!!!!!!!!!!!!有一个bug，日志文件现在只能写入同一个文件，后面需要改进

# 使用这个 需要传入一个函数名来 创建对象，依次调用
class Mylog():
    # path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    def __init__(self, name):
        self.name = name
        _formater = logging.Formatter('%(message)s')
        self.logzeros = logzero
        # self.logzeros.setup_logger(name=str(uuid.uuid1()),logfile=(Mylog.path + self.name + ".log"),formatter=_formater,maxBytes=10000000,backupCount=6)
        self.logzeros.logfile(filename=(self.name + ".log"), formatter=_formater,
                             maxBytes=1000000000, backupCount=6)
    def debug(self, message):
        self.logzeros.logger.debug(message)

    def info(self, message):
        self.logzeros.logger.info(message)

    def warn(self, message):
        self.logzeros.logger.warn(message)

    def error(self, message):
        self.logzeros.logger.error(message)


if __name__ == '__main__':
    My = Mylog("test")
    My.debug("debug test")
    My.debug("this is test")