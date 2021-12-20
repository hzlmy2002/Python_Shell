from apps.stream import Stream
from apps.decorators import argumentLimit, hasParam, notEmpty
from apps.exceptions import InvalidFileOrDir
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
    args = stream.getArgs()
    rootPath = "."
    if len(args) == 1:
        rootPath = args[0]
        if not (os.path.exists(rootPath) and os.path.isdir(rootPath)):
            raise InvalidFileOrDir(f"Directory {rootPath} does not exist")
    pattern = stream.getParam("name")
    stdout = stream.getStdout()
    relativePaths = findFiles(rootPath, pattern)
    stdout.write(relativePaths)
