from typing import Callable
from apps import cat, cd, cut, echo, find, grep, head, ls, pwd, sort, stream, tail, uniq
from apps.decorators import unsafe


class AppNotFoundError(RuntimeError):
    pass


def appFactory(appName: str) -> Callable[["stream.Stream"], None]:
    appTable = {
        "cat": cat.cat,
        "cd": cd.cd,
        "cut": cut.cut,
        "echo": echo.echo,
        "find": find.find,
        "grep": grep.grep,
        "head": head.head,
        "ls": ls.ls,
        "pwd": pwd.pwd,
        "sort": sort.sort,
        "tail": tail.tail,
        "uniq": uniq.uniq,
    }

    if appName in appTable:
        return appTable[appName]
    elif appName.startswith("_") and not appName[1:].startswith("_"):
        return unsafe(appFactory(appName[1:]))
    else:
        raise AppNotFoundError(f"Application {appName} not found.")
