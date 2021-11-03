from apps.App import App
import re

class Grep(App):
    def __init__(self) -> None:
        super().__init__()
        

    def match_line(self, filename, filelen, pattern):
        """Finds matching pattern given by args and Append to output"""
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                if re.match(pattern, line) and filelen <= 1:
                    self.outputs.append(line)
                else:
                    self.outputs.append(f"{filename}:{line}")

    def exec(self):
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
        return self.outputs