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

# 端口来自 https://proxy.mimvp.com/stat.php#open 统计
PORT_LIST = [8080, 3128, 80, 53281, 4145, 1080, 8118, 8081, 9999,
             8060, 23500, 8888, 9000, 9991, 41258, 808, 83, 443,
             54321, 8181, 63141, 20183, 4153, 64312, 8082, 82,
             9090, 9797, 6666, 8090, 4550, 8000, 8088]

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
