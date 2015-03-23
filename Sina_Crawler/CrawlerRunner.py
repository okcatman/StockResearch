# -*- encoding:utf-8 -*-

import requests
import re
from Fetcher import Fetcher
from CrawlerController import WebCrawler

import threading

'''

个股点评
http://finance.sina.com.cn/column/ggdp.shtml

大盘评述
http://roll.finance.sina.com.cn/finance/zq1/gsjsy/index.shtml


'''

class CrawlerRuner(object):

    def __init__(self):
        pass


    def start(self,target):
        tmp = list()
        tmp.append(target)
        thr_global = threading.Thread(target=self.__go,args=(tmp))
        thr_global.start()


    def __go(self,target):

        crawler = WebCrawler()

        # 得到连接
        crawler.set_target(target)
        target_map = crawler.get_page_link()
        # for row in target_map:
        #     for item in row:
        #         print item,
        #     print ""


        #多线程得到内容
        f = Fetcher(threads=10)

        for row in target_map:
            if row[0].startswith(r"http://finance.sina.com.cn"):
                f.push({'target': row[0],'type':0})
            elif row[0].startswith(r"http://licaishi.sina.com.cn"):
                f.push({'target': row[0],'type':1})
            elif row[0].startswith(r"http://blog.sina.com.cn"):
                tmp_index = row[0].rfind("?")
                if tmp_index != -1:
                    tmp_target = row[0][:tmp_index]
                    f.push({'target': tmp_target,'type':2})
                else:
                    f.push({'target': row[0],'type':2})
            elif row[0].startswith(r"http://guba.sina.com.cn"):
                    f.push({'target': row[0],'type':3})



        while f.task_left():
            res_map = f.pop()
            print res_map['target']
            print res_map['info']
            print "****************************************************"




if __name__ == "__main__":

    runner = CrawlerRuner()
    # 大盘评述
    runner.start(r"http://roll.finance.sina.com.cn/finance/zq1/gsjsy/index.shtml")
    # 个股评述
    runner.start(r"http://finance.sina.com.cn/column/ggdp.shtml")












