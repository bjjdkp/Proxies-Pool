# --*-- coding:utf-8 --*--

"""
Download and generate source ips.
"""

import re
import pymongo
import requests
from db import mongo
from settings import *
from tqdm import tqdm
from utils.gen_ip import GenIps
from utils.file_downloader import Downloader


source_ips_path = SOURCE_IPS_PATH


def _get_ip_count():
    """
    match ip list from delegated-apnic-latest
    :return: a list such as
                    (organisation, start_ip, ip_count) (CN,223.255.0.0,32768)
    """
    ip_count = []
    with open(source_ips_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        line_search = re.search(
            r'apnic\|(.*?)\|ipv4\|(.*?)\|(.*?)\|\d+\|[allocated|assigned]+',
            line)
        if not line_search:
            continue
        organisation = line_search.group(1)
        start_ip = line_search.group(2)
        ip_count_value = line_search.group(3)
        if organisation == "CN":
            ip_count.append((organisation, start_ip, ip_count_value))

    return ip_count


def _gen_source_ip(collection):
    """
    gen source ip and save to database
    :param collection: collection name for source ips
    :return:
    """
    index = 0
    remote_index = collection.count()
    ip_count = _get_ip_count()

    with tqdm(
            bar_format="{postfix[0]} {postfix[1][value]:>5}",
            postfix=["Estimated ips count:", dict(value=0)]
    ) as t:

        for ip_item in ip_count:
            ip_list = GenIps().gen(ip_item[1], ip_item[2])
            if (remote_index - index) < 1000000:
                for ip in tqdm(ip_list, desc="inserting source ips"):
                    try:
                        collection.insert_one({
                            "host": ip,
                            "host_status": 0,
                            "scan_status": 0,
                            "check_status": 0,
                        })
                    except pymongo.errors.DuplicateKeyError as e:
                        pass
                    finally:
                        t.postfix[1]["value"] += 1
                        t.update()
            else:
                index += len(ip_list)
                t.postfix[1]["value"] = index
                t.update()


def _get_apnic_file():
    # not used for now
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
    Downloader(APNIC_URL).download()
    _gen_source_ip(mongo_conn)
    mongo.Mongo().init_index(collection_name)
