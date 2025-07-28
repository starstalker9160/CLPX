from flask import Flask
from flask_sock import Sock
import json, threading, time


app = Flask(__name__)
sock = Sock(app)


@app.route('/')
def home():
    return "Hello from Flask on LAN!"

@sock.route('/ws')
def websocket(ws):
    print('WebSocket connection established.')
    while True:
        data = ws.receive()
        if data is None:
            break
        print(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6262)