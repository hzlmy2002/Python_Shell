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
    if path.is_dir():
        stream.setWorkingDir(os.path.normpath(path.__str__()))
    else:
        raise InvalidFileOrDir("Directory does not exist")
