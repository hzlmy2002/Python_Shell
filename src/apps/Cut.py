from apps.stream import Stream
from apps.decorators import hasParam, notEmpty
from apps.exceptions import InvalidArgumentError, InvalidParamError, MissingStdin
from apps.tools import getLines
from typing import List


def checkDigit(n: str):
    return n.isdigit() and int(n) >= 1


def parseByteRange(param: str) -> "List[int]":
    res = param.split("-")
    if len(res) == 1:
        if checkDigit(res[0]):
            # single positioned (e.g. 2)
            index = int(res[0])
            return [index - 1, index]
    elif len(res) == 2:
        if all(checkDigit(element) for element in res):
            # has a start and end (e.g. 1-4)
            li = [int(res[0]) - 1, int(res[1])]
            if li[1] < li[0]:
                raise InvalidArgumentError(
                    f"{li[1]}-{li[0]}Given range should not be decreasing"
                )
            return li

        if checkDigit(res[0]) and res[1] == "":
            # no end (e.g. 5-)
            return [int(res[0]) - 1, -1]

        # no start (e.g. -5)
        return [0, int(res[1])]

    raise InvalidParamError(f"Invalid parameter {param}")


def readBytesOfLine(byterange: "List[int]", line: str) -> str:
    if byterange == [0, 1]:
        return line[byterange[0]]
    start = byterange[0]
    end = byterange[1]
    if end == -1:
        end = len(line)
    return "".join(line[start:end])


def isBiggerEqual(x: int, y: int):
    # make -1 act like inf
    if x == -1:
        return True
    return x >= y


def fixByteRanges(byteRanges: "List[List[int]]"):
    # fix duplicates and byte ranges that
    # includes others
    # (e.g. 1-5 and 3, where 1-5 includes byte 3)
    bR = byteRanges.copy()
    bR.sort()
    res = [bR[0]]
    for ele in bR:
        if isBiggerEqual(res[-1][1], ele[0]):
            if ele[1] == -1 or res[-1][1] == -1:
                res[-1][1] = -1
            else:
                res[-1][1] = max(res[-1][1], ele[1])
        else:
            res.append([ele[0], ele[1]])
    return res


def parseParamArguments(paramArgs: str) -> "List[str]":
    res = [ele.strip() for ele in paramArgs.split(",")]

    if "" in res:
        raise InvalidParamError(f"Invalid parameter format {paramArgs}")
    return res


@notEmpty
@hasParam("b", required=True)
def cut(stream: "Stream"):
    stdout = stream.getStdout()
    paramArgs = parseParamArguments(stream.getParam("b"))
    if len(stream.getArgs()) == 0:
        stdin = stream.getStdin()
        if stdin is None:
            raise MissingStdin("Missing stdin")
        lines = stdin.readlines()
    else:
        lines = getLines(stream)
    byteRanges = fixByteRanges([parseByteRange(element) for element in paramArgs])
    res = ""
    for line in lines:
        for byterange in byteRanges:
            res += readBytesOfLine(byterange, line)
        if not res.endswith("\n"):
            res += "\n"
    stdout.write(res)
