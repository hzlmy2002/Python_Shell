from apps.Stream import Stream


def echo(stream: "Stream"):
    stdout = stream.getStdout()
    stdout.write(" ".join(stream.getArgs()) + "\n")
