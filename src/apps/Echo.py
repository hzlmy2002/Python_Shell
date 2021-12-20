from apps.stream import Stream
from apps.decorators import glob


@glob
def echo(stream: "Stream"):
    stdout = stream.getStdout()
    output = []
    for i in stream.getArgs():
        output.append(i)
    out = " ".join(output)
    stdout.write(out + "\n")
