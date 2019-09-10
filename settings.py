# --*-- coding:utf-8 --*--

# databases
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB_SOURCE = "proxy"
MONGO_COLLECTION_SOURCE = "ip_source"
MONGO_COLLECTION_HTTP = "http"
MONGO_COLLECTION_HTTPS = "https"
MONGO_USR = "test"
MONGO_PWD = "test"

# score for proxy
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

# specify ports for scanning, such as ["22", "80", "8080", "10000-20000"]
PORT_LIST = ["1-65535"]

# check url
# TODO: build check server
HTTP_CHECK_URL = "http://httpbin.org/get?show_env=1"
HTTPS_CHECK_URL = "https://httpbin.org/get?show_env=1"

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"

# apnic file url
APNIC_URL = "http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest"
# file path for source ips download from apnic
SOURCE_IPS_PATH = "files/source-ips.txt"

# default weight for proxies
DEFAULT_WEIGHT = 30

# local_settings
try:
    from local_settings import *
except ImportError:
    pass

