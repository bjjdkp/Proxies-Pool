# --*-- coding:utf-8 --*--

# 代理检测
# TODO: 写入操作
# TODO：两个库，http 和 https

# TODO：判定是否扫描过，判定是否进行过代理检测

import requests
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

    def check_ips(self, ip, port):
        """
        check proxy toward http and https protocol
        :param ip:
        :param port:
        :return:
        """

        url = "http://httpbin.org/get?show_env=1"
        headers = {
            'User-Agent': USER_AGENT,
        }

        proxies = {
            "http": "http://%s:%s" % (ip, port),
            "https": "https://%s:%s" % (ip, port),
        }
        try:
            res = requests.get(url, headers=headers, proxies=proxies, timeout=10)
        except requests.exceptions.ConnectTimeout:
            print("ERROR: ConnectTimeout [%s, %s]" % (ip, port))
        except requests.exceptions.ProxyError:
            print("ERROR: ProxyError [%s, %s]" % (ip, port))
        except requests.exceptions.ReadTimeout:
            print("ERROR: ReadTimeout [%s, %s]" % (ip, port))
        except Exception as e:
            print("ERROR: %s [%s, %s]" % (e, ip, port))
        else:
            print("SUCCESS: [%s, %s, %s]" % (res.status_code, ip, port))


