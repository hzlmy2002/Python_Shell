from apps.App import App
import re


class Grep(App):
    """
    STREAM:
    app = grep
    param = [REGEX]
    args = [FILENAME, FILNAME2....]  stores the file names specified"""

    def __init__(self) -> None:
        super().__init__()

    def match_line(self, filename, pattern):
        """Finds matching pattern given by args returns matched lines"""
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                if re.match(pattern, line):
                    if len(self.args) > 1:
                        self.matched.append(f"{filename}:{line}")
                    else:
                        self.matched.append(line)

    def exec(self, stream: "Stream") -> "Stream":
        self.stream = stream
        self.matched = []
        pattern = self.param[0]
        for filename in self.args:
            self.match_line(filename, pattern)
        if not self.matched[-1].endswith("\n"):
            self.matched.append("\n")
        return self.matched

    """def exec(self):
        self.outputs = []
        print(self.args)
        if len(self.args) < 2:
            raise ValueError("wrong number of command line arguments")
        pattern = self.args[0]
        files = self.args[1:]
        filelen = len(files)
        for filename in files:
            self.match_line(filename, filelen, pattern)
        print(self.outputs)
        return self.outputs"""
