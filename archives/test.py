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

# try:
#     # a = 2/0
#     res = requests.get('https://www.google.com/', timeout=3)
# except TimeoutError as e:
#     print(e)
# # except requests.exceptions.ConnectionError as e:
# #     print(e)
# # except ZeroDivisionError as e:
# #     print(e)
# else:
#     print(res)


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

print(collection.count())