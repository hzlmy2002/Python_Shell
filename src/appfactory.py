from apps import *


class AppNotFoundError(RuntimeError):
    pass


def appFactory(appName: str) -> "App":
    if appName == "pwd":
        return Pwd()
    elif appName == "echo":
        return Echo()
    elif appName == "cd":
        return Cd()
    elif appName == "cat":
        return Cat()
    elif appName == "ls":
        return Ls()
    elif appName == "head":
        return Head()
    elif appName == "tail":
        return Tail()
    elif appName == "grep":
        return Grep()
    elif appName == "cut":
        return Cut()
    elif appName == "find":
        return Find()
    elif appName == "uniq":
        return Uniq()
    elif appName == "sort":
        return Sort()
    else:
        raise AppNotFoundError("Application not found.")
