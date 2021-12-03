from typing import Callable
from apps import *
from apps.Sort import sort
from apps.decorators import unsafe


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
    if appName == "sort":
        return sort
    if appName == "uniq":
        return uniq
    if appName == "tail":
        return tail
    if appName.startswith("_"):
        return unsafe(appFactory(appName[1:]))

    raise AppNotFoundError("Application not found.")
