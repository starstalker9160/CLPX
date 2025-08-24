from flask import Flask
from flask_sock import Sock

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

            # Log received message
            print(f"Received: {data}")

            # Broadcast to all clients
            dead_clients = []
            for client in clients:
                try:
                    client.send(data)
                    print(f"Sent: {data.encode('utf-8')}")
                except:
                    dead_clients.append(client)

            # Remove dead clients
            for client in dead_clients:
                clients.discard(client)
    finally:
        clients.discard(ws)
        print(f"Client disconnected: {ws}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6262)
