# --*-- coding:utf-8 --*--

from db import mongo
from flask import Flask, g, request


app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'mongodb'):
        g.mongodb = mongo.Mongo()
    return g.mongodb


@app.route('/')
def index():
    """
    考虑返回usage,处于安全考虑，暂时放弃
    """
    return '404'


@app.route('/get-one')
def get_one():
    """
    从权重前1/3随机返回一个代理
    :return:
    """
    protocol = request.args.get('protocol')
    conn = get_conn().get_one(protocol)
    return conn


@app.route('/get-all')
def get_all():
    """
    Get a proxy
    :return: 随机代理
    """
    protocol = request.args.get('protocol')
    conn = get_conn().get_all(protocol)
    return {"data": conn}


@app.route('/count')
def get_count():
    """
    Get the count of proxies
    :return: 代理池总量
    """
    protocol = request.args.get('protocol')
    count = get_conn().get_conn(protocol).count_documents({})
    return str(count)


if __name__ == '__main__':
    app.run(debug=True)
