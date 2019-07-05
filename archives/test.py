import requests
import pymongo

# url = "http://123.206.38.21:5555/"
# headers = {
#     "X-Real-Ip": "11.11.11.11",
#     "X-Forwarded-For": "22.22.22.22",
# }
# proxies = {
#         # 高匿
#         "http": "http://180.104.107.46:45700",
#         "https": "https://180.104.107.46:45700",
#
#         # 透明
#         # "http": "http://123.139.56.238:9999",
#         # "https": "https://123.139.56.238:9999",
#
#     }
# res = requests.get(url, headers=headers, proxies=proxies)
# print(res.text)


mongo_user = "test"
mongo_pwd = "test"
host = "localhost"
db_name = "proxy"
collection_name = "ip_source"
client = pymongo.MongoClient(host)
db = client[db_name]
db.authenticate(mongo_user, mongo_pwd,
                 mechanism='SCRAM-SHA-1')
collection = db[collection_name]

print(collection.estimated_document_count())
try:
    collection.update_many(
            {}, {"$unset": {"checked_ports": "", "check_status": ""}},
            upsert=False,
        )

    # res = collection.find({"check_times":  {"$ne": 12}}).count()
    # print(res)
except pymongo.errors.DuplicateKeyError as e:
    print(e)
print(collection.estimated_document_count())

# index1 = pymongo.IndexModel([("host", 1)], unique=True)
# index2 = pymongo.IndexModel([("host_status", 1)])
# collection.create_indexes([index1, index2])

# collection.create_index([("host", 1)], unique=True)

# collection.drop_indexes()
# for i in collection.list_indexes():
#     print(i)
