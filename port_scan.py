# --*-- coding:utf-8 --*--

import re
import json
import time
import nmap
# import aiohttp
import asyncio
# import socket
import datetime
# import requests
import pymongo
import requests
from utils.genips import GenIps
from config import *
from itertools import product


class ProxyPool(object):

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
        match ip list from delegated-apnic-latest
        :return: a list such as (organisation, start_ip, ip_count) (CN,223.255.0.0,32768)
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

    async def scan_ip(self, ip):
        """
        scan ip by nmap
        :param ip:
        :return:
        """
        async with self.semaphore:
            print("start scanning ip:%s" % ip)
            nm = nmap.PortScanner()
            port_str = ",".join([str(x) for x in self.port_list])
            scan_res = await self.loop.run_in_executor(None, nm.scan, ip, port_str)

            self.parse_save_scaninfo(ip, scan_res)
            return scan_res

    def parse_save_scaninfo(self, ip, scan_info):
        """
        parse and save scan info to database
        :param ip
        :param scan_info:
        :return:
        """

        scan_stats = scan_info["nmap"]["scanstats"]
        host_status = int(scan_info["nmap"]["scanstats"]["uphosts"])
        ports = scan_info["scan"].get(ip)["tcp"] if host_status else {}
        if ports:  # 原始数据key为int
            for key in ports.keys():
                ports[str(key)] = ports.pop(key)

        now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        data = {
            "host": ip,
            "scan_stats": scan_stats,
            "host_status": host_status,
            "ports": ports,
            "updated_time": now_time
        }
        self.collection.update_one(
            {"host": data["host"]}, {"$set": data},
            upsert=False,
        )
        print("%s complete" % ip)

    def contrast_data(self, host):
        """
        judge the data is exist
        :param host: ip
        :return: whether the res in database
        """

        original_date = self.collection.find_one({"host": host})
        if not original_date:
            return "not exist"
        else:
            return "exist"

    def ip_source(self):
        index = 0
        remote_index = self.collection.count()
        ip_count = self.get_ip_count()
        for ip_item in ip_count:
            # ip_list.extend(GenIps().gen(ip_item[1], ip_item[2]))
            ip_list = GenIps().gen(ip_item[1], ip_item[2])
            # 写入数据库
            print(index)
            if (remote_index - index) < 100000:
                for ip in ip_list:
                    if self.contrast_data(ip) == "exist":
                        print("%s exists..." % ip)
                        continue
                    else:
                        print(ip)
                        self.collection.insert({"host": ip, "check_times": 0})
            else:
                index += len(ip_list)

    def pre_scan(self):
        """
        读取ip，准备扫描
        :return:
        """
        while self.collection.find({"host_status": None}):
            ip_list = self.collection.find({"host_status": None}, {"host": 1, "_id": 0}).limit(10000)
            ip_list = [i["host"] for i in ip_list]

            # 扫描开放端口 协程
            self.loop = asyncio.get_event_loop()
            self.semaphore = asyncio.Semaphore(500)
            tasks = [self.scan_ip(ip) for ip in ip_list]
            self.loop.run_until_complete(asyncio.wait(tasks))



    def pre_check(self):
        """
        从ip_source中过滤有开放端口的ip
        # TODO： ports不为空 添加标识字段
        :return:
        """
        ip_list = self.collection.find({"host_status": 1}, {"_id": 0}, no_cursor_timeout=True).limit(10000)
        for ip_info in ip_list:
            ip = ip_info["host"]
            ports = ip_info["ports"].keys()
            for item in product([ip], ports):
                self.check_proxy(item[0], item[1])


    def run(self):


        # 保存apnic开放给中国的所有ip
        # self.ip_source()

        # 扫描ip
        # start_time = time.time()
        # self.pre_scan()
        # end_time = time.time()
        # print('Cost time:', end_time - start_time)

        # 代理检测
        # TODO: 写入操作
        # TODO：两个库，http 和 https
        # self.pre_check()

        # 批量更改字段
        # TODO：判定是否扫描过，判定是否进行过代理检测
        # self.collection.update_many({}, {'$set': {'check_times': 0}})
        # mongo索引
        # self.collection.create_index("check_times")

if __name__ == '__main__':
    proxy_test = ProxyPool()
    proxy_test.run()
