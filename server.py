import sys, subprocess, socket, threading

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

def getLocalIP() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def getNormalized(value: str) -> str: return value.replace('\r\n', '\n').replace('\r', '\n')

def udpListener():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 6969))
    print("Listening for discovery")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"[UDP] Received: {data} from {addr}")
        if data == "DISCOVER_clpx.services.homelab.ree".encode("utf-8"):
            sock.sendto(f"{getLocalIP()}:{6262}/".encode(), addr)

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
    try:
        threading.Thread(target=udpListener, daemon=True).start()
        app.run(host='0.0.0.0', port=6262)
    except KeyboardInterrupt:
        print("Program interrupted by user")
