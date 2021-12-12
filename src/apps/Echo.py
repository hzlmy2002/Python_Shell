from apps.Stream import Stream


def echo(stream: "Stream"):
    stdout = stream.getStdout()
    output = []
    for i in stream.getArgs():
        output.append(i)
    out = " ".join(output)
    stdout.write(out + "\n")
