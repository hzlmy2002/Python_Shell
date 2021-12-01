class StdOutForTest:
    def __init__(self):
        self.output = ""

    def write(self, s: str):
        self.output += s

    def getOut(self):
        return self.output
