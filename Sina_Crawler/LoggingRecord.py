#coding:utf-8

import logging
import logging.config
import sys

class LogRec(object):


    # 不是配置文件的
    @staticmethod
    def start_logging():
        # 生成一个日志对象
        logger = logging.getLogger("start")
        # 成一个格式器，用于规范日志的输出格式。如果没有这行代码，那么缺省的
        # 格式就是："%(message)s"。也就是写日志时，信息是什么日志中就是什么，
        # 没有日期，没有信息级别等信息。logging支持许多种替换值，详细请看
        formatter = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S')
        # 生成一个Handler。logging支持许多Handler，
        # 象FileHandler, SocketHandler, SMTPHandler等，我由于要写
        # 文件就使用了FileHandler。
        file_handler = logging.FileHandler("merge.log")
        # 将格式器设置到处理器上
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler(sys.stderr)
        # 将处理器加到日志对象上
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        # 设置日志信息输出的级别。logging提供多种级别的日志信息，如：NOTSET,
        # DEBUG, INFO, WARNING, ERROR, CRITICAL等。每个级别都对应一个数值。
        # 如果不执行此句，缺省为30(WARNING)。可以执行：logging.getLevelName
        # (logger.getEffectiveLevel())来查看缺省的日志级别。日志对象对于不同
        # 的级别信息提供不同的函数进行输出，如：info(), error(), debug()等。当
        # 写入日志时，小于指定级别的信息将被忽略。因此为了输出想要的日志级别一定
        # 要设置好此参数。这里我设为NOTSET（值为0），也就是想输出所有信息
        # logger.setLevel(logging.ERROR)

        logger.debug("debug message")
        logger.info("info message")
        logger.warn("warn message")
        logger.error("error message")
        logger.critical("critical message")

    isLoadConf = False
    # 利用配置文件的
    @staticmethod
    def get_logger(name):
        #create logger
        if not LogRec.isLoadConf:
            LogRec.isLoadConf = True
            logging.config.fileConfig("logging.conf")
        return logging.getLogger(name)

        # #"application" code
        # logger.debug("debug message")
        # logger.info("info message")
        # logger.warn("warn message")
        # logger.error("error message")
        # logger.critical("critical message")

