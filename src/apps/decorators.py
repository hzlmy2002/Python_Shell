from typing import Callable
from apps.Exceptions import MissingParamError
from apps.Stream import Stream
from apps.Exceptions import *


def hasArgument(call: Callable[["Stream"], None]):
    def wrapper(stream: "Stream"):
        if not stream.getArgs():
            raise InvalidArgumentError("Should take arguments")
        call(stream)

    return wrapper


def noArgument(call: Callable[["Stream"], None]):
    def wrapper(stream: "Stream"):
        if stream.getArgs():
            raise InvalidArgumentError("Should not take arguments")
        call(stream)

    return wrapper


def paramTag(intendKey):
    # If it has a key then it must be of value intendKey
    def decoratorParamTag(call: Callable[["Stream"], None]):
        def wrapper(stream: "Stream"):
            args = stream.getArgs()
            if args:
                key = args[0]
                if key[0] == "-" and key[1:] != intendKey:
                    raise InvalidParamTagError(f"Invalid tag {key}")
            call(stream)

        return wrapper

    return decoratorParamTag


def intParam(key, required=False, defaultVal=0):
    def decoratorIntParam(call: Callable[["Stream"], None]):
        def wrapperIntParam(stream: "Stream"):
            args = stream.getArgs()
            try:
                i = args.index("-" + key)
                val = args[i + 1]
                stream.removeArg(i)
                stream.removeArg(i)
            except (ValueError, IndexError) as e:
                if isinstance(e, IndexError):
                    raise MissingParamError(f"Missing argument for parameter {key}")
                elif required:
                    raise MissingParamError(f"Missing parameter {key}")
                else:
                    val = defaultVal
            stream.addParam(key, val)
            call(stream)

        return wrapperIntParam

    return decoratorIntParam
