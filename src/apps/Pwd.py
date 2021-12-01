from apps.stream import Stream


def pwd(stream: "Stream") -> None:
    workingDir = stream.getEnv("workingDir")
    stream.getStdout().write(workingDir + "\n")
