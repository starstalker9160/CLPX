from utils import *
from classes import *
import socket, threading
from flask_sock import Sock
from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest


app = Flask(__name__)
sock = Sock(app)
cnfg = getConfig()

activeDevices = {}
clipHist = ClipHist(enableLimit=True, limit=50)

userGroups = []


def udpListener():
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', cnfg["udpPort"]))
        log("Listening for discovery")

        while True:
            data, addr = sock.recvfrom(1024)
            print(f"[UDP] Received: {data} from {addr}")
            if data == cnfg["discoverMessage"].encode("utf-8"):
                ip = getLocalIP()
                response = f"{ip}:{cnfg["serverPort"]}".encode()
                sock.sendto(response, addr)


@app.route('/')
def home():
    return "hello world"

@app.route('/whoami')
def whoami(): return cnfg["service"]

@app.route(cnfg["URLs"]["newUserGroup"])
def newUserGroup(): return "fuck you"

@app.route(cnfg["URLs"]["register"], methods=["POST"])
def register():
    # TODO:
    # please fix this shit or i will be sad :(

    # this shit is obsolete,
    # make this work with the new client object
    # need to do usergroup validation, authorization and shit
    # please for the love of all that is holy
    return Exception("FUCK YOU")
    try:
        data = request.get_json()
    except BadRequest:
        return jsonify({"status": "error", "message": "Invalid JSON format"}), 400

    if (
        not data
        or {"deets", "passwrd"} - set(data.keys())
        or not isinstance(data["deets"], dict)
        or {"os", "ip", "port"} - set(data["deets"].keys())
    ):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    if data["passwrd"] != "topSecretPassword":
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    ip = data["ip"]

    activeDevices[ip] = {
        "registeredAt": dt.datetime.now(dt.timezone.utc).isoformat()
    }

    log(f"Device {ip} added to activeDevices", 1)

    return jsonify({"status": "success", "message": f"Device {ip} registered"}), 200

@sock.route(cnfg["URLs"]["websocket"])
def websocket(ws):
    while True:
        data = ws.receive()
        print(data)


if __name__ == '__main__':
    threading.Thread(target=udpListener, daemon=True).start()
    app.run(host='0.0.0.0', port=cnfg["serverPort"])
