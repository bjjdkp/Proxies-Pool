# --*-- coding:utf-8 --*--

import time
import random
import datetime
from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/')
def index():
    # headers = request.headers
    # print(headers)
    r = random.uniform(1, 10)
    time.sleep(r)
    # response = make_response('Hello World')
    # response.set_cookie('Name', 'hah', max_age=3600)

    return str(r)


if __name__ == '__main__':
    app.run(threaded=True)
