from typing import Callable
from apps.stream import Stream
from commandtree import Call


class MissingParamError(RuntimeError):
    pass


def intParam(key, required=False, defaultVal=0):
    def decoratorIntParam(call: Callable[["Stream"], None]):
        def wrapperIntParam(stream: "Stream"):
            args = stream.getArgs()
            try:
                i = args.index("-" + key)
                val = args[i + 1]
                stream.removeArg(i)
                stream.removeArg(i)
            except ValueError:
                if required:
                    raise MissingParamError(f"Missing parameter {key}")
                else:
                    val = defaultVal
            stream.addParam(key, val)
            call(stream)

        return wrapperIntParam

    return decoratorIntParam
