from typing import Callable
from apps import *


class AppNotFoundError(RuntimeError):
    pass


def appFactory(appName: str) -> Callable[["Stream"], None]:
    if appName == "pwd":
        return pwd
    if appName == "head":
        return head
    if appName == "echo":
        return echo
    if appName == "cat":
        return cat
    if appName == "cd":
        return cd
    if appName == "ls":
        return ls
    if appName == "cut":
        return cut
    if appName == "find":
        return find
    if appName == "grep":
        return grep

    raise AppNotFoundError("Application not found.")
