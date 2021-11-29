from typing import Callable

from commandtree import Call
from apps.stream import Stream
from apps.pwd import pwd


class AppNotFoundError(RuntimeError):
    pass


def appFactory(appName: str) -> Callable[["Stream"], None]:
    if appName == "pwd":
        return pwd

    raise AppNotFoundError("Application not found.")
