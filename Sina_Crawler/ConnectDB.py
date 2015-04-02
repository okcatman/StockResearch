# -*- coding: utf8 -*-
import MySQLdb
import threading
import traceback
from LoggingRecord import LogRec
from Config import Config
import sys

class ConnectDB:
    instance={}
    thr=threading.Lock()
    def __init__(self):
        pass

    #获取数据库连接
    @staticmethod
    def get_con(db_no):
        try:
            if(not ConnectDB.instance.has_key(db_no)):# 如果实例中没有该连接，则创建
                db_config=Config.MYSQL[db_no] # 获取配置文件中连接信息
                ConnectDB.thr.acquire()   # 加锁
                if(not ConnectDB.instance.has_key(db_no)):# 避免加锁时，实例被创建，再次检验
                    ConnectDB.instance[db_no]=MySQLdb.connect(host=db_config["host"],user=db_config["uname"],passwd=db_config["pwd"],db=db_config["db_name"],port=db_config["port"],charset=db_config["encoding"])
                    ConnectDB.instance[db_no].autocommit = True # 如果你设为false，在commit之前，所有的sql就像一个事务 对数据库伤害较大
                    ConnectDB.thr.release()
            return ConnectDB.instance[db_no]
        except Exception,ex:
            ConnectDB.thr.release()
            LogRec.get_logger(Config.ERRLOGGER).error(traceback.print_exc())

    #创建新连接
    @staticmethod
    def get_pool_conn(db_no):
        try:
            ConnectDB.thr.acquire()   # 加锁
            db_config=Config.MYSQL[db_no] # 获取配置文件中连接信息
            conn =MySQLdb.connect(host=db_config["host"],user=db_config["uname"],passwd=db_config["pwd"],db=db_config["db_name"],port=db_config["port"],charset=db_config["encoding"])
            conn.autocommit = True # 如果你设为false，在commit之前，所有的sql就像一个事务 对数据库伤害较大
            ConnectDB.thr.release()
            return conn
        except Exception,ex:
            info = sys.exc_info()
            err_logger = LogRec.get_logger(Config.ERRLOGGER)
            for file, lineno, function, text in traceback.extract_tb(info[2]):
                err_str = file, "line:", lineno, "in", function
                err_logger.error(err_str)
            err_str = "** %s: %s" % info[:2]
            err_logger.error(err_str)

    @staticmethod
    def delete_con(db_no):
        try:
            if(ConnectDB.instance.has_key(db_no)):
                ConnectDB.thr.acquire()
                ConnectDB.instance[db_no].close()
                del(ConnectDB.instance[db_no])
                ConnectDB.thr.release()
        except Exception,ex:
            ConnectDB.thr.release()
            LogRec.get_logger(Config.ERRLOGGER).error(traceback.print_exc())

    @staticmethod
    def get_encoding(db_no):
        db_config=Config.MYSQL[db_no]
        return db_config["encoding"]

    def __del__(self):
        ConnectDB.thr.acquire()
        if(len(ConnectDB.instance)):
            for each in ConnectDB.instance:
                each.close()
            ConnectDB.instance={}
        ConnectDB.thr.release()

