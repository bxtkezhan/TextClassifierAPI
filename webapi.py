#! /usr/bin/env python3
from flask import Flask, jsonify, request, render_template

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import socket

import config as C
import json
import time

from fasttext import load_model

clf = load_model(C.model_path)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        text = request.form['text'].replace('\n', ' ')
        predict = clf.predict(text)[0][0]
        return predict

if __name__ == '__main__':
    flag = True
    s = socket.socket()
    try:
        s.connect(('127.0.0.1', C.port))
        s.shutdown(2)
    except:
        flag = False
        http_server = HTTPServer(WSGIContainer(app))
        http_server.listen(C.port, address='0.0.0.0')
        IOLoop.instance().start()
    finally:
        if flag: print('Port:' + str(C.port) + 'is already in use')
