# --*-- coding:utf-8 --*--

"""
Extract ips for scanning and checking in databases
"""

import pika
from settings import *


class BaseMqProducer(object):
    def __init__(self):
        credentials = pika.PlainCredentials(MQ_USR, MQ_PWD)
        conn_params = pika.ConnectionParameters(MQ_HOST, MQ_PORT, credentials=credentials)
        self.conn_broker = pika.BlockingConnection(conn_params)
        self.channel = self.conn_broker.channel()

    def close(self):
        self.conn_broker.close()


class ScanProducer(BaseMqProducer):
    def __init__(self):
        super(ScanProducer, self).__init__()
        pass




class CheckMqProducer(BaseMqProducer):
    def __init__(self):
        super(CheckMqProducer, self).__init__()
        pass




# # 通过此信道交互
# channel.exchange_declare(exchange="hello-exchange",
#                          exchange_type="direct",
#                          passive=False,
#                          durable=True,
#                          auto_delete=False
#                          )
#
# for item in range(10000):
#     msg_props = pika.BasicProperties()
#     msg_props.content_type = "text/plain"
#
#     channel.basic_publish(body=str(item),
#                           exchange="hello-exchange",
#                           properties=msg_props,
#                           routing_key="hola"
#                           )
#
#
# conn_broker.close()



