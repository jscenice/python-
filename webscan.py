# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     main.py
   Description :
   Author :       jsec
   date：          2021/12/28
-------------------------------------------------
   Change Activity:
                   2021/12/28
-------------------------------------------------
"""
__author__ = 'Jsec'
import os
import random
import time
import requests
import re
import argparse
import threading
from queue import Queue


class Scanner:
    def __init__(self,url,thread_number):
        print("*****开始工作*****")
        #初始化目录
        self.script_path = os.path.dirname(os.path.abspath(__file__))
        self.output_path = os.path.join(self.script_path,"output")
        self.dict_path = os.path.join(self.script_path,"dict")
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path,mode=0o777)
        self.url = url
        self.threadnum = thread_number
        self.lock = threading.Lock()
        self.q = Queue()
        self.Thread_stop = False
        self.load_dict()

    def load_dict(self):
        dict_path = self.dict_path+'.txt'
        with open(dict_path,'r',encoding="utf-8") as f:
            for line in f:
                if line[0:1] != "#":
                    self.q.put(line.strip())
        if self.q.qsize() >0:
            pass
        else:
            print("Dict is NUll")
            quit()

    def output_result(self,fin_result):
        localtime = time.strftime("%Y-%m-%d",time.localtime())
        result_txt = str(localtime)+".txt"
        path = self.output_path+"\\"+result_txt
        self.lock.acquire()
        with open(path,"a+") as f:
            f.write(fin_result+"\n")
        self.lock.release(

        )
    def success_result(self,fin_result):
        localtime = time.strftime("%Y-%m-%d",time.localtime())
        success_txt = str(localtime)+"success.txt"
        path = self.output_path+"\\"+success_txt
        self.lock.acquire()
        with open(path,"a+") as f:
            f.write(fin_result+"\n")
        self.lock.release(

        )
    def run (self,result_page):
        while not self.q.empty() and self.Thread_stop is False:
            url ="http://"+self.url+self.q.get()
            self.scan(url,result_page)
            time.sleep(0.1)

    def scan (self,target,exit_results):
        target = target
        exit_results = exit_results
        try:
            html_result = requests.get(target,headers=random_user_agent(True),allow_redirects= False,timeout=60)
            if exit_results != {}:

                if html_result.text:

                    if html_result.status_code != exit_results['code']:

                        if html_result.text != exit_results['content'] and len(html_result.text )!= exit_results['size']:

                            print('[%i]%s' % (html_result.status_code,html_result.url))
                            self.success_result('[%i]%s' % (html_result.status_code, html_result.url))
                            self.output_result('[%i]%s' % (html_result.status_code, html_result.url))
                        else:
                            print('[%i]%s is not exit' % (html_result.status_code,html_result.url))
                            self.output_result('[%i]%s' % (html_result.status_code,html_result.url))
                    else:
                        print('[%i]%s is not exit' % (html_result.status_code, html_result.url))
                        self.output_result('[%i]%s' % (html_result.status_code, html_result.url))
                else:

                    print('[%i]%s is not exit' % (html_result.status_code, html_result.url))
                    self.output_result('[%i]%s' % (html_result.status_code, html_result.url))
            else:

                if html_result.status_code == 200 and html_result.text:
                    print('[%i]%s' % (html_result.status_code, html_result.url))
                    self.success_result('[%i]%s' % (html_result.status_code, html_result.url))
                    self.output_result('[%i]%s' % (html_result.status_code, html_result.url))

        except requests.exceptions.ConnectionError as e:
            pass

#利用正则表达式对输入域名的判定
def is_domain(domain):
    domain_regex = re.compile(r'(?:[A-Z0-9_](?:[A-Z0-9_]{0,247}[A-Z0-9_]?\.)+(?:[A-Z]{2,6}|[A-Z0-9_]{2,}(?<!))\Z)',re.IGNORECASE)
    return True if domain_regex.match(domain) else False

#对url是否以http或者https开头做判断并处理
def is_http(url):
  if url.startswith('http://') or url.startswith('https://'):
      return url
  else:
      url = "http://"+url
      return url
def random_user_agent(flag):
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    ]
    if flag :
        headers = {
            'User-Agent':random.choice(USER_AGENTS),
            "Accept":"*/*",
            "Referer" :"http://www.baidu.com",
        }
        return headers
    else:
        headers = {
            "User-Agent":USER_AGENTS[0],
            "Accept":"*/*",
            "Referer":"http://www.baidu.com",

        }
        return headers

def find_page(url):
    wrong_page = ["/shanhe.html","/yuyuyu.html"]
    test_page = wrong_page[0]
    target = url+test_page
    print("******* checking %s 404 page*****" %target)
    result = {}
    try:
        req = requests.get(target,headers=random_user_agent(True),verify=False,timeout = 60)
        req_content = req.text
        result = {
            "code":req.status_code,
            "size":len(req_content),
            "content":req_content
        }
    except requests.exceptions.ConnectionError as e:
        print(e)
    return result


if __name__ == '__main__':
    url = input("请输入网址")
    if url.startswith("http://") or url.startswith("https://"):
        url = url.split("/")
        if is_domain(url[2]):
            result_conten = find_page(is_http(url[2]))
            scan = Scanner(url[2],1)
            for i in range(5):
                t = threading.Thread(target=scan.run,args=(result_conten,))
                t.setDaemon(True)
                t.start()
            while True:
                if threading.activeCount() <=1:
                    break
                else:
                    try:
                        time.sleep(1)
                    except KeyboardInterrupt as e:
                        print("\n[WARNING] User aborted,wait all slave threads to exit,current(%i)" % threading.activeCount())
                        scan.Thread_stop = True
            print("扫描结束")