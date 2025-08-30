import sys, subprocess, socket, threading
import tokens

try:
    from flask import Flask
    from flask_sock import Sock
    import mysql.connector
except ImportError as e:
    missing = e.name
    pkg = {"flask": "flask", "flask_sock": "flask-sock", "mysql": "mysql-connector-python"}.get(missing, missing)
    print(f"Missing module: {missing} (pip package: {pkg})")
    o = input(f"Install {pkg}? (y/n): ").strip().lower()
    if o == "y":
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        print(f"{pkg} installed. Please rerun the script.")
    else:
        sys.exit(1)


def init_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password=tokens.fuckMySQL, # the password is a secret because i hate myself just enough to hide it...
            database="clipboard_db"
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clipboard_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        return conn
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        sys.exit(1)

db_conn = init_db()
db_cursor = db_conn.cursor()


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
    while True:
        try:
            sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock_udp.bind(('', 6969))
            print("Listening for discovery")

            while True:
                data, addr = sock_udp.recvfrom(1024)
                print(f"[UDP] Received: {data} from {addr}")
                if data == "DISCOVER_clpx.services.homelab.ree".encode("utf-8"):
                    sock_udp.sendto(f"{getLocalIP()}:{6262}/".encode(), addr)
        except Exception as e:
            print("Fatal: udpListener encountered an error")
            print(e)
            sys.exit(1)

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

            try:
                # mind you, i have no idea what the fuck this does
                # i read the documentation and when i ran the code, it didnt give me an error so die lit?
                db_cursor.execute("INSERT INTO clipboard_history (content) VALUES (%s)", (data,))
                db_conn.commit()
            except mysql.connector.Error as err:
                print(f"MySQL insert error: {err}")

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
        sys.exit(1)
