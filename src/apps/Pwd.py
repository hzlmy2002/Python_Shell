from apps.stream import Stream


def pwd(stream: "Stream") -> None:
    workingDir = stream.getWorkingDir()
    stream.getStdout().write(workingDir + "\n")
