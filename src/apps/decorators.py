import os
from typing import Callable
from apps.Exceptions import InvalidParamError, MissingParamError
from apps.Stream import Stream
from apps.Exceptions import InvalidArgumentError, InvalidParamTagError
import traceback
from pathlib import Path


# def atMostOneArgument(call: Callable[["Stream"], None]):
#     def wrapper(stream: "Stream"):
#         if len(stream.getArgs()) != 0 and len(stream.getArgs()) != 1:
#             raise InvalidArgumentError("Exceeded maximum amount of argument required")
#         call(stream)

#     return wrapper


# def hasOneArgument(call: Callable[["Stream"], None]):
#     def wrapper(stream: "Stream"):
#         if len(stream.getArgs()) != 1 or stream.getArgs()[0] == "":
#             raise InvalidArgumentError("Should take a single argument")
#         call(stream)

#     return wrapper


# def hasArgument(call: Callable[["Stream"], None]):
#     def wrapper(stream: "Stream"):
#         if not stream.getArgs() or stream.getArgs()[0] == "":
#             raise InvalidArgumentError("Argument required but not supplied")
#         call(stream)

#     return wrapper


# def noArgument(call: Callable[["Stream"], None]):
#     def wrapper(stream: "Stream"):
#         if stream.getArgs():
#             raise InvalidArgumentError("Should not take arguments")
#         call(stream)

#     return wrapper


def notEmpty(call: Callable[["Stream"], None]):
    def wrapper(stream: "Stream"):
        if not stream.getArgs():
            raise InvalidArgumentError("Should not take empty arguments")
        call(stream)

    return wrapper


def argumentLimit(limit=0, strict=True):
    # Strict implies number of arguments must == limit
    # When not strict, number of arguments can vary between 0-limit inclusive
    # Default to strictly 0
    def decorator(call: Callable[["Stream"], None]):
        def wrapper(stream: "Stream"):
            length = len(stream.getArgs())
            if (strict and length != limit) or (
                not strict and not (length >= 0 and length <= limit)
            ):
                raise InvalidArgumentError("Invalid Number of arguments")
            call(stream)

        return wrapper

    return decorator


def onlyParamTag(intendKey):
    # If it has a key then it must be of value intendKey
    def decoratorParamTag(call: Callable[["Stream"], None]):
        def wrapper(stream: "Stream"):
            args = stream.getArgs()
            if args:
                key = args[0]
                if len(key) < 2 or (key[0] == "-" and key[1:] != intendKey):
                    raise InvalidParamTagError(f"Invalid tag {key}")
            call(stream)

        return wrapper

    return decoratorParamTag


def hasParam(key: str, required: bool, defaultVal=0, numeric=False):
    def decoratorHasParam(call: Callable[["Stream"], None]):
        @onlyParamTag(key)
        def wrapperIntParam(stream: "Stream"):
            args = stream.getArgs()
            try:
                i = args.index("-" + key)
                val = args[i + 1]
                if not val.isnumeric() and numeric:
                    raise InvalidParamError(f"Invalid parameter argument {val}")
                stream.removeArg(i)
                stream.removeArg(i)
            except (ValueError, IndexError):
                if required:  # and Value Error
                    raise MissingParamError(f"Missing parameter {key}")
                else:
                    val = defaultVal
            stream.addParam(key, val)
            call(stream)

        return wrapperIntParam

    return decoratorHasParam


def getFlag(key: str):
    def decoratorGetFlag(call: Callable[["Stream"], None]):
        @onlyParamTag(key)
        def wrapper(stream: "Stream"):
            args = stream.getArgs()
            try:
                i = args.index("-" + key)
                stream.addFlag(args[i][1])
                stream.removeArg(i)
            except (ValueError, IndexError):
                pass
            call(stream)

        return wrapper

    return decoratorGetFlag


def unsafe(call: Callable[["Stream"], None]):
    def wrapper(stream: "Stream"):
        stdout = stream.getStdout()
        try:
            call(stream)
        except Exception:
            stdout.write(traceback.format_exc())

    return wrapper


def _glob(call: Callable[["Stream"], None]):
    def wrapper(stream: "Stream"):
        workingDir = stream.getWorkingDir()
        args = stream.getArgs()
        for i in range(len(args)):
            a = args[i]
            if "*" in a:
                path = Path(workingDir)
                globbed = list(path.glob(a))
                if len(globbed) == 0:
                    print("no glob")
                    return
                stream.removeArg(i)
                for g in globbed:
                    stream.addArg(os.path.relpath(g, path))
        call(stream)

    return wrapper
