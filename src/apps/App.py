from Stream import Stream


class App:
    def __init__(self) -> None:
        # Pretty useless for now, may need it further in development
        self.app = None
        self.param = None
        self.args = None
        self.env = None

    def setter(self, input_stream):
        self.args = input_stream.get_args()
        self.param = input_stream.get_param()
        self.args = input_stream.get_args()
        self.env = input_stream.get_env

    """
    def pack_output(self):
        raise NotImplementedError("Please Implement this method")"""

    def exec(self):
        # exec should return an output list
        raise NotImplementedError("Please Implement this method")
