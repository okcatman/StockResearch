# -*- encoding:utf-8 -*-

import requests
import re
from Fetcher import Fetcher
from CrawlerController import WebCrawler
from MySqlDAL import MySqlDAL
import threading
import sys
from Config import Config
from LoggingRecord import LogRec
import traceback
import time
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

'''

个股点评
http://finance.sina.com.cn/column/ggdp.shtml

大盘评述
http://roll.finance.sina.com.cn/finance/zq1/gsjsy/index.shtml

'''

class CrawlerRuner(object):

    table_name = 'comment_info'

    type_1_lock = threading.Lock()
    type_0_lock = threading.Lock()

    def __init__(self):
        pass



    def start(self,target,category=0):
        LogRec.get_logger(Config.INFLOGGER).info(u"类型为"+str(category)+u"，开始下一轮检查并捕获信息")
        tmp = list()
        tmp.append(target)
        tmp.append(category)
        thr_global = threading.Thread(target=self.__go,args=(tmp))
        thr_global.start()


    def __go(self,target,category=0):

        if category == 0:
            self.type_0_lock.acquire()
        elif category == 1:
            self.type_1_lock.acquire()

        try:

            sqlUtil = MySqlDAL()

            LogRec.get_logger(Config.INFLOGGER).info(u"开始抓取文章链接。。。")
            crawler = WebCrawler()

            # 得到连接
            crawler.set_target(target)
            tmp_link_list = crawler.get_page_link()

            # 过滤数据库中已有的信息
            target_tuple = list()

            for row in tmp_link_list:
                tmp_link = row[0].strip()
                # 过滤blog情况
                if tmp_link.startswith(r"http://blog.sina.com.cn"):
                    tmp_index = tmp_link.rfind("?")
                    if tmp_index != -1:
                        tmp_link = tmp_link[:tmp_index]

                tmp_sql = "SELECT * FROM "+self.table_name+" WHERE target='"+tmp_link+"'"
                if not sqlUtil.get_dimensions_one_row(tmp_sql):
                    target_tuple.append(row)
                # else:
                #     print "already"


            # for row in target_tuple:
            #     for item in row:
            #         print item,
            #     print ""

            LogRec.get_logger(Config.INFLOGGER).info(u"获取最新链接列表,准备开始捕获文章内容")

            #多线程得到内容
            f = Fetcher(threads=10)

            for row in target_tuple:
                if row[0].startswith(r"http://finance.sina.com.cn"):
                    f.push({'target': row[0].strip(),'type':0,'title':row[1].strip(),'publish_time':row[2].strip()})
                elif row[0].startswith(r"http://licaishi.sina.com.cn"):
                    f.push({'target': row[0].strip(),'type':1,'title':row[1].strip(),'publish_time':row[2].strip()})
                elif row[0].startswith(r"http://blog.sina.com.cn"):
                    tmp_index = row[0].rfind("?")
                    if tmp_index != -1:
                        tmp_target = row[0][:tmp_index]
                        f.push({'target': tmp_target.strip(),'type':2,'title':row[1].strip(),'publish_time':row[2].strip()})
                    else:
                        f.push({'target': row[0].strip(),'type':2,'title':row[1].strip(),'publish_time':row[2].strip()})
                elif row[0].startswith(r"http://guba.sina.com.cn"):
                        f.push({'target': row[0].strip(),'type':3,'title':row[1].strip(),'publish_time':row[2].strip()})



            LogRec.get_logger(Config.INFLOGGER).info(u"准备写入数据库")

            while f.task_left():
                res_map = f.pop()

                #print res_map['info']
                self.__write_to_db(sqlUtil,res_map,category)

                time.sleep(0.5)

            sqlUtil.destory()

            LogRec.get_logger(Config.INFLOGGER).info(u"数据库写入完毕")

        except Exception,e:
            info = sys.exc_info()
            err_logger = LogRec.get_logger(Config.ERRLOGGER)

            for file, lineno, function, text in traceback.extract_tb(info[2]):
                err_str = file, "line:", lineno, "in", function
                err_logger.error(err_str)
            err_str = "** %s: %s" % info[:2]
            err_logger.error(err_str)

        if category == 0:
            self.type_0_lock.release()
        elif category == 1:
            self.type_1_lock.release()


    # 写入数据库
    def __write_to_db(self,sqlUtil,info_map,category):
        try:
            data_source={}
            data_source["target"] = info_map["target"]
            data_source["type"] = category
            data_source["info"] = info_map["info"]
            data_source["title"] = info_map["title"]
            data_source["db_insert_time"] = int(time.time())

            if category == 1:
                publish_time = str(datetime.date.today().year)+info_map["publish_time"]
                data_source["publish_time"] = datetime.datetime.strptime(publish_time,'%Y%m月%d日 %H:%M')
            elif category == 0:
                publish_time = info_map["publish_time"]
                data_source["publish_time"] = datetime.datetime.strptime(publish_time,'%Y-%m-%d %H:%M:%S')

            if sqlUtil.insert_data(data_source,self.table_name):
                print u"插入完毕"

            #print data_source["info"]
            #print data_source["publish_time"]

        except Exception,e:
            info = sys.exc_info()
            err_logger = LogRec.get_logger(Config.ERRLOGGER)

            for file, lineno, function, text in traceback.extract_tb(info[2]):
                err_str = file, "line:", lineno, "in", function
                err_logger.error(err_str)
            err_str = "** %s: %s" % info[:2]
            err_logger.error(err_str)


if __name__ == "__main__":

    runner = CrawlerRuner()

    while True:
        # 大盘评述
        runner.start(r"http://roll.finance.sina.com.cn/finance/zq1/gsjsy/index.shtml",category=1)
        # 个股评述
        runner.start(r"http://finance.sina.com.cn/column/ggdp.shtml",category=0)

        time.sleep(10*60)












