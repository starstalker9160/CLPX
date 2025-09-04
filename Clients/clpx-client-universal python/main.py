import socket
from utils import *

cnfg = getConfig()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.settimeout(5)

found = False

for attempt in range(cnfg["maxDiscoverRetries"]):
    print(f"Attempt {attempt + 1} of {cnfg["maxDiscoverRetries"]}...")
    try:
        sock.sendto(cnfg["discoverMessage"].encode("utf-8"), ('255.255.255.255', cnfg["udpPort"]))
        data, addr = sock.recvfrom(1024)
        print(f"Received response from {addr}: {data.decode()}")
        found = True
        break
    except socket.timeout:
        print("No response, retrying...")

if not found:
    print("nothing found")

sock.close()
