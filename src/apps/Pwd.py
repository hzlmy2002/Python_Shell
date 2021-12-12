from apps.Stream import Stream
from apps.decorators import noArgument


@noArgument
def pwd(stream: "Stream") -> None:
    workingDir = stream.getEnv("workingDir")
    stream.getStdout().write(workingDir + "\n")
