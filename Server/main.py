from utils import *
from flask import Flask
from flask_sock import Sock
import json, threading, time


app = Flask(__name__)
sock = Sock(app)
cnfg = getConfig()


@app.route('/')
def home():
    return "hello world"

@app.route('/whoami')
def whoami():
    return cnfg["service"]

@app.route(cnfg["URLs"]["register"])
def register():
    pass

@app.route(cnfg["URLs"]["copy"])
def copy():
    pass

@sock.route(cnfg["URLs"]["websocket"])
def websocket(ws):
    while True:
        data = ws.receive()
        if data is None:
            break
        print(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6262)
