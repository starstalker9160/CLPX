import json, socket
from classes import *
from platform import system as getOs


def getConfig() -> dict:
    with open('config.json', 'r') as f:
        cnfg = json.load(f)
    
    try:
        if "service" not in cnfg or "serverPort" not in cnfg or "URLs" not in cnfg:
            raise KeyError
        return cnfg
    except KeyError:
        log("Invalid config.json", 3, KeyError)


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