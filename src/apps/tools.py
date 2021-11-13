from typing import List, Dict
from Stream import *
from apps.App import App
import traceback


def isStdin(input: str) -> bool:
    """
    for any string, if it starts and ends with "\0", then it is stdin
    """
    if len(input) < 2:
        return False
    else:
        return input[0] == "\0" and input[-1] == "\0"


def str2stdin(input: str) -> str:
    """
    for any string, if it starts and ends with "\0", then it is stdin
    """
    return "\0" + input + "\0"


def stdin2str(input: str) -> str:
    """
    read stdin and return a string
    """
    if isStdin(input):
        return input[1:-1]
    else:
        return input


def unsafeDecorator(func):
    def wrapper(app: "App", stream: "Stream"):
        try:
            return func(stream)
        except Exception as e:
            tb = traceback.format_exc()
            try:
                return Stream(
                    sType=streamType.error,
                    app=stream.getApp(),
                    params=[],
                    args=[tb],
                    env={},
                )
            except Exception:
                return Stream(
                    sType=streamType.error, app="unknown", params=[], args=[tb], env={}
                )

    return wrapper
