from apps.Stream import Stream
from apps.decorators import argumentLimit, hasParam, notEmpty
from apps.Exceptions import InvalidFileOrDir
import os
import fnmatch


def findFiles(rootPath: str, pattern: str) -> str:
    result = ""
    for root, _, files in os.walk(rootPath):
        for fName in files:
            if fnmatch.fnmatch(fName, pattern):
                result += root + os.sep + fName + "\n"
    return result


@notEmpty
@hasParam("name", required=True)
@argumentLimit(1, strict=False)
def find(stream: "Stream"):
    arg = stream.getArgs()
    rootPath = "."
    if len(arg) == 1:
        rootPath = arg[0]
        if not (os.path.exists(rootPath) and os.path.isdir(rootPath)):
            raise InvalidFileOrDir("Directory does not exist")
    pattern = stream.getParam("name")
    stdout = stream.getStdout()
    relativePaths = findFiles(rootPath, pattern)
    stdout.write(relativePaths)
