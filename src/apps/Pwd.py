from apps.stream import Stream


def pwd(stream: "Stream") -> None:
    print(stream.getEnv("workingDir"))
