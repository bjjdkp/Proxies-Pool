# --*-- coding:utf-8 --*--
# TODO:选择nmap扫描或是python-nmap包扫描：速度和对当前机器的网络影响

import re
import time
import nmap
import socket
import requests
import pymongo
from libs.genips import GenIps
from config import *
from queue import Queue
from concurrent.futures import ThreadPoolExecutor



class Pool(object):

    def __init__(self):
        self.apnic_path = "./files/delegated-apnic-latest.txt"

        self.mongo_user = MONGO_USR
        self.mongo_pwd = MONGO_PWD
        self.host = MONGO_HOST
        self.db_name = MONGO_DATABASE
        self.collection_name = MONGO_COLLECTION
        self.client = pymongo.MongoClient(self.host)
        self.db = self.client[self.db_name]
        self.db.authenticate(self.mongo_user, self.mongo_pwd, mechanism='SCRAM-SHA-1')
        self.collection = self.db[self.collection_name]

        self.port_list = PORT_LIST


    def get_ip_count(self):
        """
        从delegated-apnic-latest中匹配出ip列表
        :return: 列表(organisation, start_ip, ip_count) (CN,223.255.0.0,32768)
        """
        ip_count = []
        with open(self.apnic_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            line_search = re.search(r'apnic\|(.*?)\|ipv4\|(.*?)\|(.*?)\|\d+\|[allocated|assigned]+', line)
            if not line_search:
                continue
            organisation, start_ip, ip_count_value = line_search.group(1), line_search.group(2), line_search.group(3)
            if organisation == "CN":
                ip_count.append((organisation, start_ip, ip_count_value))

        return ip_count

    def scan_ip(self, ip):
        """
        使用nmap扫描ip端口是否开放
        :param ip:
        :return:
        """
        nm = nmap.PortScanner()
        port_str = ",".join([str(x) for x in self.port_list])
        res = nm.scan(ip, port_str)
        print(res)

    def run(self):
        ip_list = []
        ip_count = self.get_ip_count()
        for ip_item in ip_count[200:300]:
            ip_list.extend(GenIps().gen(ip_item[1], ip_item[2]))

        # 写入数据库
        for ip in ip_list:
            print(ip)
            self.collection.insert({"host": ip})

        # 扫描开放端口
        # for ip in ip_list:
        #     self.scan_ip(ip)


# nm = nmap.PortScanner()
# ret = nm.scan('115.239.210.26', '1-10000')
# print(ret)

if __name__ == '__main__':
    proxy_test = Pool()
    proxy_test.run()
