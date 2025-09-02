import json, socket
from classes import *
from platform import system as getOs


def getConfig() -> dict:
    with open('config.json', 'r') as f:
        cnfg = json.load(f)
    
    try:
        if (
            {"service", "serverPort", "URLs"} - set(cnfg.keys())
            or not isinstance(cnfg["URLs"], dict)
            or {"register", "newUserGroup", "websocket"} - set(cnfg["URLs"].keys())
        ):
            raise KeyError
        return cnfg
    except KeyError:
        log("Invalid config.json, missing required fields", 3, KeyError)

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

def addUser(userData) -> Client:
    return Client(userData["ip"], userData["userGroup"])
