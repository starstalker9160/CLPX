import datetime as dt
from __future__ import annotations


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


def isOfSchema(data: dict, schema: dict) -> bool:
    if not isinstance(data, dict):
        return False

    if len(data) != len(schema):
        return False

    for key in schema:
        if key not in data:
            return False

        expected_type = schema[key]
        value = data[key]

        if isinstance(expected_type, dict):
            if not isOfSchema(value, expected_type):   # schema is pretty shallow, this is negligible in terms of time complexity, still O(n)
                return False
        else:
            if not isinstance(value, expected_type):
                return False

    return True



class ClipItem:
    def __init__(self, value: str, idempotencyKey: str):
        if not idempotencyKey:
            log("Missing idempotency key", 3)

        self._data = {
            "type": type(value).__name__,
            "value": value
        }
        self.idempotency_key = idempotencyKey

    @property
    def value(self) -> dict:
        return self._data

    def __repr__(self):
        return (f"ClipItem(type={self._data['type']!r}, value={self._data['value']!r}, "
                f"idempotency_key={self.idempotency_key!r})")


class ClipHist:
    def __init__(self, enableLimit: bool = False, limit: int = 10):
        self._items: list[ClipItem] = []
        self.enableLimit = enableLimit
        self.limit = limit

    def add(self, value: str) -> None:
        if self._items and self._items[0].value["value"] == value:
            return

        self._items.insert(0, ClipItem(value))

        if self.enableLimit and len(self._items) > self.limit:
            self._items = self._items[:self.limit]

    @property
    def current_copied(self) -> dict | None:
        return self._items[0].value if self._items else None

    def get_history(self) -> list[ClipItem]:
        return self._items

    def __repr__(self):
        return f"ClipHist({self._items!r})"


class Client:
    def __init__(self, ip: str, userGroup: UserGroup | None = None):
        self.registeredAt = dt.datetime.now(dt.timezone.utc).timestamp()

        self.ip = ip   # using this to identify each client uniquely, sorta a "client id"
        self.userGroup = userGroup

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.ip == other.ip   # see what i mean? "client id"
        else:
            return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def addedToUserGroup(self, userGroupID: UserGroup) -> None:
        if not userGroupID:
            self.userGroup = userGroupID

    def removedFromUserGroup(self) -> None:
        self.userGroup = None


class UserGroup:
    def __init__(self, userGroupID: int):
        self.id = userGroupID
        self.activeClients = []
        self.deadClients = []

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self.id == other.id
        else:
            return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def addClient(self, clientObject: Client) -> None:
        if clientObject in self.deadClients:
            self.deadClients.remove(clientObject)
        self.activeClients.append(clientObject)
        clientObject.addedToUserGroup(self)

    def removeClient(self, clientObject: Client) -> None:
        if clientObject in self.activeClients:
            self.activeClients.remove(clientObject)
            clientObject.removedFromUserGroup()
            self.deadClients.append(clientObject)
