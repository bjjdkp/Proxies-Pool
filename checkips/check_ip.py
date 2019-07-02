# --*-- coding:utf-8 --*--

# 代理检测

import json
import asyncio
import aiohttp
import datetime
from db import mongo
from config import *
from itertools import product


class CheckIps(object):
    def __init__(self):
        self.collection_source = mongo.Mongo().get_conn(MONGO_COLLECTION_SOURCE)
        self.collection_http = mongo.Mongo().get_conn(MONGO_COLLECTION_HTTP)
        self.collection_https = mongo.Mongo().get_conn(MONGO_COLLECTION_HTTPS)
        self.http_check_url = HTTP_CHECK_URL
        self.https_check_url = HTTPS_CHECK_URL

    def _pre_check(self):
        """
        提取出未检测的端口
        :return:
        """
        while self.collection_source.find({"check_status": {"$ne": 1}}):
            ip_list = self.collection_source.find({"check_status": {"$ne": 1}, "host_status": 1}, {"_id": 0}).limit(10000)
            ip_list = list(ip_list)
            if len(ip_list) < 10000:
                # TODO: 初次全量检测后的策略
                pass

            for ip_info in ip_list:
                ip = ip_info["host"]
                ports_list = ip_info["ports"].keys()
                check_ports = self.collection_source.find_one({"host": ip}).get("check_ports", [])
                ports_list = [p for p in ports_list if p not in check_ports]
                if not ports_list:
                    continue

                tasks = [self.check_ip(item[0], item[1]) for item in product([ip], ports_list)]
                self.loop = asyncio.get_event_loop()
                # self.semaphore = asyncio.Semaphore(500)
                self.loop.run_until_complete(asyncio.wait(tasks))

    async def check_ip(self, ip, port):
        http_url = self.http_check_url
        https_url = self.https_check_url
        headers = {
            'User-Agent': USER_AGENT,
        }

        proxies = {
            "http": "http://%s:%s" % (ip, port),
            "https": "https://%s:%s" % (ip, port),
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=http_url, headers=headers, proxies=proxies, timeout=10
            ) as resp:
                await self.check_res(resp, ip, port)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=https_url, headers=headers, proxies=proxies, timeout=10
            ) as resp:
                await self.check_res(resp, ip, port)

    async def check_res(self, response, ip, port):
        check_ports = self.collection_source.find_one({"host": ip}).get("check_ports", [])
        if port not in check_ports:
            check_ports.append(port)
            self.collection_source.update_one(
                {"host": ip}, {"$set": {"check_ports": check_ports}},
                upsert=False,
            )
        if response.status != 200:
            return

        res = json.loads(response.text())
        protocol_dict = {
            "80": "http",
            "443": "https",
        }

        anonymity = 1 if res["headers"]["X-Real-Ip"] == ip else 0

        if protocol_dict[res["headers"]["X-Forwarded-Port"]] == "80":
            mongo_conn = self.collection_http
        elif protocol_dict[res["headers"]["X-Forwarded-Port"]] == "443":
            mongo_conn = self.collection_https

        mongo_conn.insert({
            "ip": ip,
            "port": port,
            "anonymity": anonymity,
            "check_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        })

    # def check_ip(self, ip, port):
    #     """
    #     check proxy toward http and https protocol
    #     :param ip:
    #     :param port:
    #     :return:
    #     """
    #
    #     url = "http://httpbin.org/get?show_env=1"
    #     headers = {
    #         'User-Agent': USER_AGENT,
    #     }
    #
    #     proxies = {
    #         "http": "http://%s:%s" % (ip, port),
    #         "https": "https://%s:%s" % (ip, port),
    #     }
    #     try:
    #         res = requests.get(url, headers=headers, proxies=proxies, timeout=10)
    #     except requests.exceptions.ConnectTimeout:
    #         print("ERROR: ConnectTimeout [%s, %s]" % (ip, port))
    #     except requests.exceptions.ProxyError:
    #         print("ERROR: ProxyError [%s, %s]" % (ip, port))
    #     except requests.exceptions.ReadTimeout:
    #         print("ERROR: ReadTimeout [%s, %s]" % (ip, port))
    #     except Exception as e:
    #         print("ERROR: %s [%s, %s]" % (e, ip, port))
    #     else:
    #         print("SUCCESS: [%s, %s, %s]" % (res.status_code, ip, port))

    def run(self):
        self._pre_check()


if __name__ == '__main__':
    test = CheckIps()
    test.run()
