# --*-- coding:utf-8 --*--

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

    def save_data(self, collection_name, data):
        self.db[collection_name].insert(data)

    def init_index(self, collection_name):
        index1 = pymongo.IndexModel([("host", 1)], unique=True)
        index2 = pymongo.IndexModel([("host_status", 1)])
        index3 = pymongo.IndexModel([("check_status", 1)])
        self.db[collection_name].create_indexes([index1, index2, index3])





