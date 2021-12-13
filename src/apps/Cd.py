from apps.Stream import Stream
from apps.Exceptions import InvalidFileOrDir
from apps.decorators import hasOneArgument
from pathlib import Path


@hasOneArgument
def cd(stream: "Stream"):
    changeDir = stream.getArgs()[0]
    workingDir = stream.getWorkingDir()
    path = Path(workingDir, changeDir)
    if path.is_dir():
        stream.setWorkingDir(path.__str__())
    else:
        raise InvalidFileOrDir("Directory does not exist")
