from typing import Callable

from apps.stream import Stream
from apps.pwd import pwd
from apps.head import head
from apps.echo import echo


class AppNotFoundError(RuntimeError):
    pass


def appFactory(appName: str) -> Callable[["Stream"], None]:
    if appName == "pwd":
        return pwd
    if appName == "head":
        return head
    if appName == "echo":
        return echo

    raise AppNotFoundError("Application not found.")
