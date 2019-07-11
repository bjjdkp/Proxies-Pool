# --*-- coding:utf-8 --*--

import random
import pymongo
from config import *


class Mongo(object):

    def __init__(self):
        self.mongo_user = MONGO_USR
        self.mongo_pwd = MONGO_PWD
        self.host = MONGO_HOST
        self.db_name = MONGO_DB_SOURCE
        self.client = pymongo.MongoClient(self.host)
        self.db = self.client[self.db_name]
        self.db.authenticate(self.mongo_user, self.mongo_pwd,
                             mechanism='SCRAM-SHA-1')

    def get_conn(self, collection_name):
        return self.db[collection_name]

    def add(self, collection_name, data):
        """
        添加数据
        :param collection_name:
        :param data:
        :return:
        """
        self.db[collection_name].insert_one(data)

    def delete(self, collection_name, ip, port):
        """
        删除数据
        :return:
        """

        """
        只针对 http 和 https 表
        单ip可能存在多个port情况，
            匹配到多条数据时，删除被封端口
            匹配到单条数据时，删除被封端口，source库对应ip block_times 字段+1
            block_times 字段大于3时host_status 置为0
        """
        self.db[collection_name].find_one_and_delete({"ip": ip, "port": port})
        ip_count = self.db[collection_name].count_documents({"ip": ip})

        if not ip_count:
            ip_info = self.db[MONGO_COLLECTION_SOURCE].find_one({"host": ip})
            block_times = ip_info.get("block_times", 0)
            if block_times > 3:
                self.db[MONGO_COLLECTION_SOURCE].update_one(
                    {"host": ip},
                    {"$set": {"host_status": 0}},
                )
            else:
                self.db[MONGO_COLLECTION_SOURCE].update_one(
                    {"host": ip},
                    {"$inc": {"block_times": 1}},
                )

    def get_one(self, collection_name):
        """
        从权重前1/3中随机返回一个
        :return:
        """
        ip_list = list(self.db[collection_name].find({}, {"_id": 0}))
        if not ip_list:
            print("代理池枯竭了。。。")
            return
        ip_list.sort(key=lambda x: x["weight"], reverse=True)
        pick_range = ip_list[:len(ip_list)//3]
        return random.choice(pick_range)

    def get_all(self, collection_name):
        """
        返回所有数据
        :return:
        """
        ip_list = self.db[collection_name].find({}, {"_id": 0})
        return list(ip_list)

    def block(self, collection_name, ip, port):
        """
        ip在某一网站被封，权重减1，权重为0,删除
        :return:
        """
        self.db[collection_name].update_one(
            {"ip": ip, "port": port},
            {"$inc": {"weight": -1}},
        )
        ip_info = self.db[collection_name].find_one({"ip": ip, "port": port})
        if ip_info["weight"] == 0:
            self.delete(collection_name, ip, port)

    def max(self, collection_name, ip, port):
        """
        代理可用，权重提升到100
        :param collection_name:
        :param ip:
        :param port:
        :return:
        """
        self.db[collection_name].update_one(
            {"ip": ip, "port": port},
            {"$set": {"weight": 100}},
        )

    def init_index(self, collection_name):
        """
        初始化索引
        :return:
        """
        if collection_name in ["http", "https"]:
            index1 = pymongo.IndexModel([("host", 1)])
        else:
            index1 = pymongo.IndexModel([("host", 1)], unique=True)
        index2 = pymongo.IndexModel([("host_status", 1)])
        index3 = pymongo.IndexModel([("check_status", 1)])
        self.db[collection_name].create_indexes([index1, index2, index3])


if __name__ == '__main__':
    test = Mongo()
    test.init_index('http')


