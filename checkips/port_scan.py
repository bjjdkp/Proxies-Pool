# --*-- coding:utf-8 --*--

import nmap
import asyncio
import datetime
from config import *
from db import mongo


class PortScan(object):

    def __init__(self):
        self.source_ips_path = SOURCE_IPS_PATH
        self.collection = mongo.Mongo().get_conn(MONGO_COLLECTION_SOURCE)
        self.port_list = PORT_LIST

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
            {"host": data["host"]}, {"$set": data, "$inc": {"scan_times": 1}},
            upsert=False,
        )
        print("scan complete: %s" % ip)

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

    def pre_scan(self):
        """
        读取ip，准备扫描
        :return:
        """
        while self.collection.find({"host_status": None}):
            ip_list = self.collection.find({"host_status": None}, {"host": 1, "_id": 0}).limit(10000)
            ip_list = list(ip_list)
            if len(ip_list) < 10000:
                # TODO: 初次全量扫描后的策略
                pass
            ip_list = [i["host"] for i in ip_list]

            # 扫描开放端口
            self.loop = asyncio.get_event_loop()
            self.semaphore = asyncio.Semaphore(500)
            tasks = [self.scan_ip(ip) for ip in ip_list]
            self.loop.run_until_complete(asyncio.wait(tasks))


    def run(self):

        # scan ips
        self.pre_scan()


if __name__ == '__main__':
    proxy_test = PortScan()
    proxy_test.run()
