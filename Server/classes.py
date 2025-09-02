from typing import Any
import datetime as dt


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

    def add(self, value: str):
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
    def __init__(self, ip, userGroup):
        self.registeredAt = dt.datetime.now(dt.timezone.utc).timestamp()

        self.ip = ip
        self.userGroup = userGroup
