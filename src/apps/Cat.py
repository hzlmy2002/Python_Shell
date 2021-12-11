from typing import List, Dict
from apps.Exceptions import InvalidFileOrDir
from apps.decorators import hasArgument
from .Stream import *
from io import StringIO


@hasArgument
def cat(stream: "Stream"):
    fileNames = stream.getArgs()
    stdout = stream.getStdout()
    content = ""
    for file in fileNames:
        try:
            if type(file) == StringIO:
                content += file.getvalue()

            else:
                with open(file, "r") as f:
                    content += f.read()
            if not content.endswith("\n"):
                content += "\n"
        except FileNotFoundError:
            raise InvalidFileOrDir(f"File {file} does not exist")
    stdout.write(content)
