import json, socket
from platform import system as getOs


def log(msg: str, code: int = 0, exceptionType: type[BaseException] = Exception) -> None:
    """
    Prints a formatted log message or raises an exception for failures

    Args:
        msg (str): The message to log or include in the exception
        code (int, optional): The log level code; Defaults to 0
            - 0: OK
            - 1: INFO
            - 2: WARN
            - 3: FAIL (raises Exception or specified exception with formatted message)
        exceptionType (type, optional): Exception type to raise if code is 3. Defaults to Exception

    Raises:
        exceptionType: If `code` is 3, raises this exception type with the formatted message
    """
    labels = {0: (" OK ", 32), 1: ("INFO", 34), 2: ("WARN", 33), 3: ("FAIL", 31)}
    tag, color = labels.get(code, ("???? ", 37))
    formatted_msg = f"\033[37m[\033[0m \033[{color}m{tag}\033[0m \033[37m] {msg}\033[0m"

    if code == 3:
        raise exceptionType(formatted_msg) from None
    else:
        print(formatted_msg)


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