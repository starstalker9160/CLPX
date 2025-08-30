import sys, subprocess

try:
    from flask import Flask
    from flask_sock import Sock
except ImportError as e:
    missing = e.name
    pkg = {"flask": "flask", "flask_sock": "flask-sock"}.get(missing, missing)
    print(f"Missing module: {missing} (pip package: {pkg})")
    o = input(f"Install {pkg}? (y/n): ").strip().lower()
    if o == "y":
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        print(f"{pkg} installed. Please rerun the script.")
    else:
        sys.exit(1)

app = Flask(__name__)
sock = Sock(app)

clients = set()

@sock.route('/ws')
def websocket(ws):
    clients.add(ws)
    print(f"Client connected: {ws}")
    try:
        while True:
            data = ws.receive()
            if data is None:
                break

            print(f"Received: {data}")

            dead_clients = []
            for client in clients:
                try:
                    client.send(data)
                    print(f"Sent: {data.encode('utf-8')}")
                except:
                    dead_clients.append(client)

            for client in dead_clients:
                clients.discard(client)
    finally:
        clients.discard(ws)
        print(f"Client disconnected: {ws}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6262)
