# --*-- coding:utf-8 --*--

# 代理检测

import time
import json
import asyncio
# import aiohttp
import requests
import datetime
from db import mongo
from config import *
from itertools import product
from collections import Counter


class CheckIps(object):
    def __init__(self):
        self.collection_source = mongo.Mongo().get_conn(MONGO_COLLECTION_SOURCE)
        self.collection_http = mongo.Mongo().get_conn(MONGO_COLLECTION_HTTP)
        self.collection_https = mongo.Mongo().get_conn(MONGO_COLLECTION_HTTPS)
        self.http_check_url = HTTP_CHECK_URL
        self.https_check_url = HTTPS_CHECK_URL

    def _pre_check(self):
        # while self.collection_source.find({"check_status": {"$ne": 1}}):
            ip_list = self.collection_source.find({"check_status": {"$ne": 1}, "host_status": 1}, {"_id": 0}).limit(10)
            ip_list = list(ip_list)
            if len(ip_list) < 1000:
                # TODO: 初次全量检测后的策略
                pass

            tasks = []
            for ip_info in ip_list:
                ip = ip_info["host"]
                ports_list = ip_info["ports"].keys()
                checked_ports = self.collection_source.find_one({"host": ip}).get("checked_ports", [])
                ports_list = [p for p in ports_list if p not in checked_ports]
                if not ports_list:
                    continue

                tasks.extend([asyncio.ensure_future(self.check_ip(item[0], item[1])) for item in product([ip], ports_list)])

            print(tasks)
            self.loop = asyncio.get_event_loop()
            # self.semaphore = asyncio.Semaphore(500)
            self.loop.run_until_complete(asyncio.wait(tasks))

    def send_req(self, url=None, proxies=None):
        headers = {
            'User-Agent': USER_AGENT,
        }
        try:
            return requests.get(url=url,
                                headers=headers,
                                proxies=proxies,
                                timeout=10)
        except requests.exceptions.ConnectTimeout:
            print("ERROR: ConnectTimeout %s" % proxies)
        except requests.exceptions.ProxyError:
            print("ERROR: ProxyError %s" % proxies)
        except requests.exceptions.ReadTimeout:
            print("ERROR: ReadTimeout %s" % proxies)
        except Exception as e:
            print("ERROR: %s %s" % (e, proxies))

    async def check_ip(self, ip, port):
        print("start check %s %s" % (ip, port))
        http_url = self.http_check_url
        https_url = self.https_check_url

        proxies = {
            "http": "http://%s:%s" % (ip, port),
            "https": "https://%s:%s" % (ip, port),
        }
        loop = asyncio.get_running_loop()
        for url in [http_url, https_url]:
            response = await loop.run_in_executor(None, self.send_req, url, proxies)
            await self.check_res(response, ip, port)

        # aiohttp 暂时不支持https代理
        # async with aiohttp.ClientSession() as session:
        #     async with session.get(
        #         url=http_url, headers=headers, proxy=proxies["http"], timeout=10
        #     ) as resp:
        #         await self.check_res(resp, ip, port)

    async def check_res(self, response, ip, port):

        checked_ports = self.collection_source.find_one({"host": ip}).get("checked_ports", [])
        opened_ports = self.collection_source.find_one({"host": ip})["ports"].keys()
        if port not in checked_ports:
            checked_ports.append(port)

        check_status = 1 if Counter(checked_ports) == Counter(opened_ports) else 0

        self.collection_source.update_one(
            {"host": ip}, {"$set": {"checked_ports": checked_ports,
                                    "check_status": check_status}},
            upsert=False,
        )

        if not response or response.status_code != 200:
            return

        try:
            res = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            return

        protocol_dict = {
            "80": "http",
            "443": "https",
        }

        anonymity = 1 if res["headers"]["X-Real-Ip"] == ip else 0

        if protocol_dict[res["headers"]["X-Forwarded-Port"]] == "80":
            mongo_conn = self.collection_http
        else:
            mongo_conn = self.collection_https

        print("SUCCESS: [%s, %s]" % (ip, port))
        mongo_conn.insert({
            "ip": ip,
            "port": port,
            "anonymity": anonymity,
            "check_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        })

    def run(self):
        s_time = time.time()
        self._pre_check()
        print("cost: %s" % (time.time() - s_time))


if __name__ == '__main__':
    test = CheckIps()
    test.run()
