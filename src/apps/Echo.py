from apps.Stream import Stream
from io import StringIO

def echo(stream: "Stream"):
    stdout = stream.getStdout()
    output=[]
    for i in stream.getArgs():
        if type(i) == StringIO:
            output.append(i.getvalue())
        else:
            output.append(i)
    out=" ".join(output)
    if out[-1] == "\n":
        stdout.write(out)
    else:
        stdout.write(out+"\n")
