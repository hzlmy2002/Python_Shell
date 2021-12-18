from typing import Callable
from apps import Cat, Cd, Cut, Echo, Find, Grep, Head, Ls, Pwd, Sort, Tail, Uniq, Stream
from apps.decorators import unsafe


class AppNotFoundError(RuntimeError):
    pass


def appFactory(appName: str) -> Callable[["Stream.Stream"], None]:
    appTable = {
        "cat": Cat.cat,
        "cd": Cd.cd,
        "cut": Cut.cut,
        "echo": Echo.echo,
        "find": Find.find,
        "grep": Grep.grep,
        "head": Head.head,
        "ls": Ls.ls,
        "pwd": Pwd.pwd,
        "sort": Sort.sort,
        "tail": Tail.tail,
        "uniq": Uniq.uniq,
    }

    if appName in appTable:
        return appTable[appName]
    elif appName.startswith("_") and not appName[1:].startswith("_"):
        return unsafe(appFactory(appName[1:]))
    else:
        raise AppNotFoundError(f"Application {appName} not found.")
