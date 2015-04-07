# encoding:utf-8
__author__ = 'Shudong Ma'

import requests
import re
import sys
from Config import Config
from LoggingRecord import LogRec
import traceback
reload(sys)
sys.setdefaultencoding('utf-8')

'''

个股点评
http://finance.sina.com.cn/column/ggdp.shtml

大盘评述
http://roll.finance.sina.com.cn/finance/zq1/gsjsy/index.shtml


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

    # rep_tag = [' ', '\t', '\n', '\r', '\f', '\v', '<div', '&nbsp;', '<a', '</a>', '<A', '</A>', '<table', '<TABLE',
    #            '</TABLE>', '</table>', '<tr', '<td', '</tr>', '<TR', '</TR>', '<TD', '</TD>', '</td>', '<p', '<span',
    #            '<P', '<SPAN', '<DIV', "&", '<font', '<B', '<b', '<br', '/>', '</div>', '</DIV>', '</p>', '</span>',
    #            '</SPAN>','<wbr>', '</font>', '</FONT>', '</B>','</P>','</img>', '<FONT', '>', 'id=','sina_keyword_ad_area2','articalContentnewfont_family','quote_','stock_']
    #
    #
    # regex_tag = {
    #     re.compile(r"href=['\"]?http://[\s\S]*?>"): "",
    #     re.compile(r"target=['\"]?[\s\S]*?['\"]?"): "",
    #     re.compile(r"class=['\"]?[\s\S]*?['\"]?"): "",
    #     re.compile(r"style=[\"][\s\S]*?[\"]"): "",
    #     re.compile(r"STYLE=[\"][\s\S]*?[\"]"): "",
    #     re.compile(r"<img[\s\S]*?>"): "",
    #     re.compile(r"FACE=['\"]?[\s\S]*?['\"]?"): "",
    #     re.compile(r"src=['\"]?.+?['\"]?"): "",
    #     re.compile(r"COLOR=['\"]?.+?['\"]?"): "",
    #     re.compile(r"<!--news_keyword.+"):"",
    # }

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
        try:
            resp = requests.get(self.__target, headers=self.headers)
            resp.encoding = 'gbk'
        except:
            info = sys.exc_info()
            err_logger = LogRec.get_logger(Config.ERRLOGGER)
            for file, lineno, function, text in traceback.extract_tb(info[2]):
                err_str = file, "line:", lineno, "in", function
                err_logger.error(err_str)
            err_str = "** %s: %s" % info[:2]
            err_logger.error(err_str)

        return resp


    # 返回获得的网页连接

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
        try:
            # 先找出div 部分，然后再在小块中匹配
            divPattern = '''<div class="listBlk">([\s\S]*?)<div class="MainBtm">'''
            div_reg = re.compile(divPattern)
            div_content = div_reg.findall(content)[0]

            infoPattern = '''<li><a href="([\s\S]*?)" target="_blank">([\s\S]*?)</a><span>\(([\S\s]*?)\)</span></li>'''
            reg = re.compile(infoPattern)
            matches = reg.findall(div_content)

        except Exception,e:
            info = sys.exc_info()
            err_logger = LogRec.get_logger(Config.ERRLOGGER)
            for file, lineno, function, text in traceback.extract_tb(info[2]):
                err_str = file, "line:", lineno, "in", function
                err_logger.error(err_str)
            err_str = "** %s: %s" % info[:2]
            err_logger.error(err_str)

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