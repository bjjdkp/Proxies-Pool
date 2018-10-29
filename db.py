# --*-- coding:utf-8 --*--

# redis

import redis

MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = "proxies"


class RedisClient(object):
    # proxies pool
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, pwd=REDIS_PASSWORD):
        """
        initial the Redis
        :param host: Redis host
        :param port: Redis port
        :param pwd: Redis password
        """

        self.db = redis.StrictRedis(host=host, port=port, password=pwd, decode_responses=True)

    def add(self, ):
        pass
