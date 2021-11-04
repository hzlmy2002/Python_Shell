class Stream:
    def __init__(self, stream_type, app, param, args, env) -> None:
        """
        self.stream_type (int) : 0 represents input, 1 represents output
        self.args (List of String)
        """
        self.stream_type = stream_type
        self.app = app
        self.param = param
        self.args = args
        self.env = env

    def get_app(self):
        return self.app

    def get_args(self):
        return self.args

    def add_env(self, env):
        self.env = env
