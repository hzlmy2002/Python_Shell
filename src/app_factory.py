from apps import *


class CommandNotFoundError(RuntimeError):
    pass


def app_factory(app_name: str) -> "App":
    if app_name == "pwd":
        return Pwd()
    elif app_name == "echo":
        return Echo()
    elif app_name == "cd":
        return Cd()
    else:
        raise CommandNotFoundError("Commmand {app_name} not recognised.")
