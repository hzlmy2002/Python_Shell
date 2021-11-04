from apps.App import App


class HeadTail(App):
    """
    STREAM:
    app = head/tail
    param = [] / ["-n"]
    args = [FILENAME] / [num_line,FILENAME] if -n specified in param"""

    def __init__(self):
        super().__init__()
        self.num_lines = None

    def file_op(self, lines):
        """Requires implementation of child class"""
        raise NotImplementedError("Please Implement this method")

    def process_stream(self) -> int:
        if not self.param:
            self.num_lines = 10
        else:
            self.num_lines = int(self.args[0])

    '''def process_args(self) -> int:
        """Process arguments passed and returns index in args of which file name is stored"""
        if len(self.args) == 1:
            self.num_lines = 10
            return 0
        if len(self.args) == 3:
            if self.args[0] != "-n":
                raise ValueError("wrong flags")
            self.num_lines = int(self.args[1])
            return 2
        raise ValueError("wrong number of command line arguments")'''

    def exec(self):
        self.output = []
        self.process_stream()
        file = self.args[-1]
        with open(file) as f:
            lines = f.readlines()
            self.file_op(lines)
        return self.output
