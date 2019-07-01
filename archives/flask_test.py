# --*-- coding:utf-8 --*--
import datetime
from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/')
def index():
    headers = request.headers
    print(headers)

    response = make_response('Hello World')
    response.set_cookie('Name', 'hah', max_age=3600)

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
