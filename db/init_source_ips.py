# --*-- coding:utf-8 --*--

"""
下载更新文件
从数据库读取

"""
import re
import pymongo
import requests
from db import mongo
from config import *
from utils.gen_ip import GenIps


source_ips_path = SOURCE_IPS_PATH


def _get_ip_count():
    """
    match ip list from delegated-apnic-latest
    :return: a list such as (organisation, start_ip, ip_count) (CN,223.255.0.0,32768)
    """
    ip_count = []
    with open(source_ips_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        line_search = re.search(
            r'apnic\|(.*?)\|ipv4\|(.*?)\|(.*?)\|\d+\|[allocated|assigned]+', line)
        if not line_search:
            continue
        organisation = line_search.group(1)
        start_ip = line_search.group(2)
        ip_count_value = line_search.group(3)
        if organisation == "CN":
            ip_count.append((organisation, start_ip, ip_count_value))

    return ip_count


def _gen_source_ip(collection):
    index = 0
    remote_index = collection.count()
    ip_count = _get_ip_count()
    for ip_item in ip_count:
        # ip_list.extend(GenIps().gen(ip_item[1], ip_item[2]))
        ip_list = GenIps().gen(ip_item[1], ip_item[2])
        print("source ip index: %s" % index)
        if (remote_index - index) < 100000:
            for ip in ip_list:
                try:
                    collection.insert({"host": ip, "scan_times": 0})
                except pymongo.errors.DuplicateKeyError as e:
                    print("ip exists: %s" % ip)
                else:
                    print("insert ip: %s" % ip)
        else:
            index += len(ip_list)


def _get_apnic_file():
    print("downloading apnic file...")
    file_url = "http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"

    with open(source_ips_path, 'wb') as f:
        r = requests.get(file_url, stream=True)
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)


def init_source_ips():
    collection_name = MONGO_COLLECTION_SOURCE
    mongo_conn = mongo.Mongo().get_conn(collection_name)
    _get_apnic_file()
    _gen_source_ip(mongo_conn)
    mongo.Mongo().init_index(collection_name)

