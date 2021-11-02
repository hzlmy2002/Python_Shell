class App:
    def __init__(self) -> None:
        # Pretty useless for now, may need it further in development
        self.out = None
        self.args = None

    def setter(self, out, args):
        self.out = out
        self.args = args

    def exec(self):
        raise NotImplementedError("Please Implement this method")
