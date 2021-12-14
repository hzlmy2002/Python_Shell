from apps.Stream import Stream
from apps.decorators import argumentLimit


@argumentLimit()
def pwd(stream: "Stream") -> None:
    workingDir = stream.getWorkingDir()
    stream.getStdout().write(workingDir + "\n")
