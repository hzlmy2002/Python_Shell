from apps.Stream import Stream
from apps.Exceptions import InvalidFileOrDir
from apps.decorators import argumentLimit
from pathlib import Path
import os


@argumentLimit(1)
def cd(stream: "Stream"):
    changeDir = stream.getArgs()[0]
    workingDir = stream.getWorkingDir()
    path = Path(workingDir, changeDir)
    pathStr = os.path.normpath(path.__str__())
    if path.is_dir():
        stream.setWorkingDir(pathStr)
    else:
        raise InvalidFileOrDir(f"Directory {pathStr} does not exist")
