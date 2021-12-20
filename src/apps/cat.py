from apps.exceptions import InvalidFileOrDir, MissingStdin
from apps.decorators import glob
from .stream import Stream


@glob
def cat(stream: "Stream"):
    fileNames = stream.getArgs()
    stdout = stream.getStdout()
    content = ""
    if len(fileNames) == 0:
        stdin = stream.getStdin()
        if stdin is None:
            raise MissingStdin("Missing stdin")
        content += stdin.read()
    else:
        for file in fileNames:
            try:
                with open(file, "r") as f:
                    content += f.read()
            except FileNotFoundError:
                raise InvalidFileOrDir(f"File {file} does not exist")
    if not content.endswith("\n"):
        content += "\n"
    stdout.write(content)
