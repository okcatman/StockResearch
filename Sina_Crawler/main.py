# encoding:utf-8

import requests
import re
from fetcher import Fetcher
import xlwt
import json
import time

from threading import Thread
from Queue import Queue
from time import sleep

'''

个股点评

</div><!--wapdump end-->
<p>　　和讯股票消息 周一卫星导航个股表现活跃，其中<span id=stock_sz300075><a href=http://finance.sina.com.cn/realstock/company/sz300075/nc.shtml class="keyword" target=_blank>数字政通</a></span><span id=quote_sz300075></span>涨停，<span id=stock_sz002405><a href=http://finance.sina.com.cn/realstock/company/sz002405/nc.shtml class="keyword" target=_blank>四维图新</a></span><span id=quote_sz002405></span>涨幅超8%，<span id=stock_sz300053><a href=http://finance.sina.com.cn/realstock/company/sz300053/nc.shtml class="keyword" target=_blank>欧比特</a></span><span id=quote_sz300053></span>涨幅超7%，<span id=stock_sz002383><a href=http://finance.sina.com.cn/realstock/company/sz002383/nc.shtml class="keyword" target=_blank>合众思壮</a></span><span id=quote_sz002383></span>涨超6%，<span id=stock_sz002465><a href=http://finance.sina.com.cn/realstock/company/sz002465/nc.shtml class="keyword" target=_blank>海格通信</a></span><span id=quote_sz002465></span>、<span id=stock_sz300036><a href=http://finance.sina.com.cn/realstock/company/sz300036/nc.shtml class="keyword" target=_blank>超图软件</a></span><span id=quote_sz300036></span>、海格通信涨幅超4%。</p>

<p>　　消息面上，3月13日下午，缅甸军机炸弹落入中方境内，造成云南省临沧市耿马县孟定镇大水桑树村正在甘蔗地作业的无辜平民4死9伤。3月13日晚，外交部副部长刘振民紧急召见缅甸驻华大使，就缅军机炸弹造成中方人员死伤提出严正交涉。</p>

<p>　　中国空军新闻发言人申进科上校3月14日早间表示，中国空军在3月13日组织多批战机起飞，对向我境抵近飞行的缅甸军机进行跟踪、监视、警告、外逼。中国空军将采取措施加强中缅边境空中应对行动，严密关注空情动态，维护国家领空主权。</p><!-- news_keyword_pub,stock,sz300036&sz300053&sz002383&sz300075&sz002405&sz002465 -->
<!-- publish_helper_end -->

'''


class WebCrawler(object):
    __target = ""
    __page = ""
    __pageCount = 1

    code_list = ['GB2312', 'GBK', 'utf-8', 'ascii', 'ANSI']

    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36',

    }

    rep_tag = [' ', '\t', '\n', '\r', '\f', '\v', '<div', '&nbsp;', '<a', '</a>', '<A', '</A>', '<table', '<TABLE',
               '</TABLE>', '</table>', '<tr', '<td', '</tr>', '<TR', '</TR>', '<TD', '</TD>', '</td>', '<p', '<span',
               '<P', '<SPAN', '<DIV', "&", '<font', '<B', '<b', '<br', '/>', '</div>', '</DIV>', '</p>', '</span>',
               '</SPAN>', '</font>', '</FONT>', '</B>', '</img>', '<FONT', '>', 'id=']

    regex_tag = {
        re.compile(r"href=['\" ]http://.+?['\" ]"): "",
        re.compile(r"target=['\" ].+?['\" ]"): "",
        re.compile(r"class=['\" ].+?['\" ]"): "",
        re.compile(r"style=['\" ].+?['\" ]"): "",
        re.compile(r"STYLE=['\" ].+?['\" ]"): "",
        re.compile(r"<img[\s\S]*?>"): "",
        re.compile(r"FACE=['\" ].+?['\" ]"): "",
        re.compile(r"src=['\" ].+?['\" ]"): "",
    }

    proxies = {
        'http': 'http://127.0.0.1:8087',
        'https': 'http://127.0.0.1:8087',
    }


    def __init__(self):
        pass

    def set_target(self, target):
        self.__target = target


    # 得到响应信息
    def get_response(self):

        resp = requests.get(self.__target, headers=self.headers, proxies=self.proxies)
        resp.encoding = 'gbk'

        return resp


    # 返回获得的网页
    def get_webpage(self):
        if self.__target == "":
            print u"请先输入目标网址"
            return
        return self.__page



    def get_page_link(self):
        if self.__target == "":
            print u"请先输入目标网址"
            return
        resp = self.get_response()
        self.link_map = self.filt_link(resp.text)
        return self.link_map




    # 过滤文章的地址
    # [(地址,标题,时间),()...]
    def filt_link(self, content):
        # 先找出div 部分，然后再在小块中匹配
        divPattern = '''<div class="listBlk">([\s\S]*?)<div class="MainBtm">'''
        div_reg = re.compile(divPattern)
        div_content = div_reg.findall(content)[0]

        infoPattern = '''<li><a href="([\s\S]*?)" target="_blank">([\s\S]*?)</a><span>\(([\S\s]*?)\)</span></li>'''
        reg = re.compile(infoPattern)
        matches = reg.findall(div_content)

        return matches


    # # 获得完整信息列表(包括表头和表体)
    # def get_table(self, type=0):
    #     if self.__target == "":
    #         print u"请先输入目标网址"
    #         return
    #     # table的存储形式是:[{"表头1":"对应数据","表头2":"对应数据"},{},...]
    #     table = []
    #     titleList = self.getTitle(type)
    #     bodyList = self.get_final_list(type)
    #     for row in bodyList:
    #         recordic = {}
    #         for i in xrange(0, len(row)):
    #             recordic[titleList[i]] = row[i]
    #         table.append(recordic)
    #     return table
    #
    # # 输出到Excel
    # def writeToExcel(self, filePath, type=0):
    #     workbook = xlwt.Workbook(encoding='utf-8')
    #     worksheet = workbook.add_sheet('sheet1')
    #     table = self.get_table(type)
    #     colnames = self.getTitle(type)
    #
    #     #输出表头
    #     i = 0
    #     for item in colnames:
    #         worksheet.write(0, i, item)
    #         i += 1
    #
    #     #输出内容
    #     index = 1
    #     for row in table:
    #         j = 0
    #         for col in colnames:
    #             worksheet.write(index, j, row[col])
    #             j += 1
    #         index += 1
    #
    #     workbook.save(filePath)


if __name__ == "__main__":

    crawler = WebCrawler()

    # 得到连接
    crawler.set_target(r"http://finance.sina.com.cn/column/ggdp.shtml")
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
            # tmp_index = row[0].rfind("?")
            # if tmp_index != -1:
            #     f.push({'target': row[0],'type':2})
            # else:
            f.push({'target': row[0],'type':2})
        elif row[0].startswith(r"http://guba.sina.com.cn"):
                f.push({'target': row[0],'type':3})


    while f.task_left():
        res_map = f.pop()
        print res_map['target']
        print res_map['info']
        print "****************************************************"









