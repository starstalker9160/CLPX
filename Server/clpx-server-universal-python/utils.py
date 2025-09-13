import json, socket
from classes import *
from platform import system as getOs


def getConfig() -> dict:
    cnfg = getDictFromJSON("config.json")

    try:
        if not isOfSchema(cnfg, Schemas.config()):
            raise KeyError
        return cnfg
    except KeyError:
        log("Invalid config.json, missing required fields", 3, KeyError)

def getLocalIP() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP

def getNormalized(value: str) -> str: return value.replace('\r\n', '\n').replace('\r', '\n')

def addUser(userData: dict) -> Client:
    if not isOfSchema(userData, Schemas.newDevice()):
        return 400
    return Client(userData["ip"], userData["userGroup"])

def getDictFromJSON(path: str) -> dict:
    with open(path, 'r') as f:
        return dict(json.load(f))