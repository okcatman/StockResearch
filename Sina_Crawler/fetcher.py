# -*- encoding:utf-8 -*-

import urllib2
from threading import Thread,Lock
from Queue import Queue
import time
import requests
import re

class Fetcher(object):


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






    def __init__(self,threads=0):
        # self.opener = urllib2.build_opener(urllib2.HTTPHandler)
        self.lock = Lock()
        self.q_task = Queue() # 任务队列  ， 存放要解决的任务的参数
        self.q_complete = Queue() # 完成队列  ，  存放需要获得的信息
        self.threads = threads # 线程数量
        for i in xrange(threads):
            t = Thread(target=self.threadget)
            t.setDaemon(True) # 设置守护进程，即主进程关闭后，子进程也强制关闭
            t.start()

        self.running = 0

    # 析构时等待两个队列完成
    def __del__(self):
        time.sleep(0.5)
        self.q_task.join()
        self.q_complete.join()

    # 剩余的任务线程
    def task_left(self):
        # 待完成的   +  已完成的  +  正在执行的
        return self.q_task.qsize() + self.q_complete.qsize() + self.running

    def push(self,req):
        self.q_task.put(req)

    def pop(self):
        return self.q_complete.get()

    def threadget(self):
        while True:
            # 默认block=True代表为阻塞式的，表示queue为空时，会等待
            req = self.q_task.get()
            complete = dict()
            with self.lock:
                # with 表示执行完后会自动解锁
                self.running += 1
            try:
                # 执行 具体任务
                # pass
                complete = self.do_main(req)

            except Exception,e:
                    print e

            self.q_complete.put(complete)
            with self.lock:
                self.running -= 1
            self.q_task.task_done()
            time.sleep(1) # 避免频繁访问，被认做垃圾连接


    # 以下配合requests使用,具体业务区..................................。。。。。。。。。。。。。。。。


    def do_main(self,req):
        resp = requests.get(req['target'],headers=self.headers,proxies=self.proxies)

        if req['type'] == 0:
            resp.encoding = 'gbk'
            content = resp.text
            pageinfo = self.filt_finance_content(content)
        elif req['type'] == 1:
            content = resp.text
            pageinfo = self.filt_licai_content(content)
        elif req['type'] == 2:
            resp.encoding = 'utf-8'
            content = resp.text
            pageinfo = self.filt_blog_content(content)
        elif req['type'] == 3:
            resp.encoding = 'gbk'
            content = resp.text
            pageinfo = self.filt_guba_content(content)

        # return pageinfo
        page_map = {'target':req['target'],'info':pageinfo}
        return page_map




    # 过滤文章内容
    def filt_finance_content(self, content):
        infoPattern = '''<!--wapdump end-->([\s\S]*?)<!-- publish_helper_end -->'''
        reg = re.compile(infoPattern)
        matches = reg.findall(content)
        res_info = ""
        if matches:
            res_info = matches[0]

            for k, v in self.regex_tag.iteritems():
                f_tmp = k.findall(res_info)
                for item in f_tmp:
                    res_info = res_info.replace(item, v)

            for item in self.rep_tag:
                res_info = res_info.replace(item, "")

        return res_info


    def filt_licai_content(self, content):

        infoPattern = '''<div class="p_article">([\s\S]*?)</div>'''
        reg = re.compile(infoPattern)
        matches = reg.findall(content)
        res_info = ""
        if matches:
            res_info = matches[0]

            for k, v in self.regex_tag.iteritems():
                f_tmp = k.findall(res_info)
                for item in f_tmp:
                    res_info = res_info.replace(item, v)

            for item in self.rep_tag:
                res_info = res_info.replace(item, "")

        return res_info

    def filt_blog_content(self, content):
        infoPattern = r'''id="sina_keyword_ad_area2"([\s\S]*?)id='share'''
        reg = re.compile(infoPattern)
        matches = reg.findall(content)

        res_info = ""
        if matches:
            res_info = matches[0]

            for k, v in self.regex_tag.iteritems():
                f_tmp = k.findall(res_info)
                for item in f_tmp:
                    res_info = res_info.replace(item, v)

            for item in self.rep_tag:
                res_info = res_info.replace(item, "")

        return res_info

    def filt_guba_content(self, content):
        infoPattern = '''<div class='ilt_p'>([\s\S]*?)<div class='ilt_panel clearfix'>'''

        reg = re.compile(infoPattern)
        matches = reg.findall(content)
        res_info = ""
        if matches:
            res_info = matches[0]

            for k, v in self.regex_tag.iteritems():
                f_tmp = k.findall(res_info)
                for item in f_tmp:
                    res_info = res_info.replace(item, v)

            for item in self.rep_tag:
                res_info = res_info.replace(item, "")

        return res_info
