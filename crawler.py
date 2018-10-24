# --*-- coding:utf-8 --*--

import redis
import requests
import pymongo
import random
from lxml import etree
from random import choice
# from bs4 import BeautifulSoup
import telnetlib


class XiCiDaiLi(object):
    """
    a spider for xicidaili
    """
    def __init__(self, proxy_type):
        self.base_url = "http://www.xicidaili.com/nn"
        self.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'zh-CN,zh;q=0.8',
            # 'Cache-Control': 'max-age=0',
            # 'Connection': 'keep-alive',
            # 'Cookie': '_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTM4ZjIxMDIzN2NmOWRiOTZkZGVjZDMyZGM4NzBiNzkwBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMXFGaUhXdldPUThYalM5Y0cwTE5lWHdrSGVMbVFDTkh2SVJub3o3Sy9nUHM9BjsARg%3D%3D--bd9ab72d429bef8411c9a696c3b439dcb4834954; Hm_lvt_0cf76c77469e965d2957f0553e6ecf59=1504164875,1504164900,1504170213; Hm_lpvt_0cf76c77469e965d2957f0553e6ecf59=1504171138',
            # 'Host': 'www.xicidaili.com',
            # 'If-None-Match': 'W/"778327b926e5449997ba176cf8c8b68d"',
            # 'Referer': 'http://www.xicidaili.com/',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        }
        self.client = pymongo.MongoClient(host="127.0.0.1", port=27017)
        self.db = self.client["ip"]
        self.sheet = self.db["usable"]

        self.proxy_type = proxy_type

    def save_result(self, usable_list):
        print(usable_list)

        self.sheet.insert(dict(usable_list), check_keys=False)

    def is_usable(self, result):
        usable_list = []
        for i in range(len(result)):
            try:
                telnetlib.Telnet(result[i][0], port=result[i][1], timeout=5)
            except:
                print("%s %s不可用" % (result[i][0], result[i][1]))
                continue
            else:
                print("%s %s可用" % (result[i][0], result[i][1]))
                item = 'http://%s:%s' % (result[i][0], result[i][1])
                res = {self.proxy_type.lower(): item}
                usable_list.append(res)

        return usable_list

    def get_ip(self):
        ip_port_list = self.sheet.find()[0].items()
        ip_port = random.choice(ip_port_list)
        return ip_port[0], ip_port[1]

    def run(self):
        print("开始爬取西刺代理...")
        html = requests.get(self.base_url, headers=self.headers).content
        # print html

        html = etree.HTML(html)
        ip_list = html.xpath('//table//tr[position()>1]/td[2]/text()')
        port_list = html.xpath('//table//tr[position()>1]/td[3]/text()')
        type_list = html.xpath('//table//tr[position()>1]/td[6]/text()')

        # 根据"HTTP"和"HTTPS"两种类型
        http_ip_list = []
        http_port_list = []
        for i in range(len(type_list)):
            if type_list[i] == self.proxy_type.upper():
                http_ip_list.append(ip_list[i])
                http_port_list.append(port_list[i])

        result = list(zip(http_ip_list, http_port_list))
        # print result
        usable_list = self.is_usable(result)
        print(usable_list)
        print("本次总共获取有效代理%s个" % len(usable_list))
        return usable_list
        # self.save_result(usable_list)


# if __name__ == "__main__":
    # spider = XiCiDaiLi("https")
    # spider.run()

    # ip, port = spider.get_ip()
    # print(ip, port)

"""
proxie = {'http': 'http://122.193.14.102:80'}   

proxies = { 
    "http": "http://"+ip,  
    "https": "https://"+ip, 
    }
"""


def test():
    url = "http://httpbin.org/get"
    proxies = {
        "http": "http://182.18.6.9:53281",
        # "https": "https://182.18.6.9:53281",
    }

    res = requests.get(url, proxies=proxies).text
    print(res)


test()

# 获取
# 存储
# 检测
# 接口


MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = "proxies"


class RedisClient(object):
    # proxies pool
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, pwd=REDIS_PASSWORD):
        """
        initial the Redis
        :param host: Redis host
        :param port: Redis port
        :param pwd: Redis password
        """

        self.db = redis.StrictRedis(host=host, port=port, password=pwd, decode_responses=True)

    def add(self, ):
        pass

