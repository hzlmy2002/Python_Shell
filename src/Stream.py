from typing import List, Dict


class Stream:
    def __init__(
        self,
        streamType: int,
        app: str,
        params: List[str],
        args: List[str],
        env: Dict[str,str],
    ) -> None:
        """
        self.stream_type (int) : 0 represents input, 1 represents output, -1 represents error
        self.app (String)
        self.param (List of String)
        self.args (List of String)
        """
        self.stream_type = streamType
        self.app = app
        self.params = params[:]
        self.args = args[:]
        self.env = env.copy()

    def getApp(self):
        return self.app

    def getParams(self):
        return self.params

    def getArgs(self):
        return self.args

    def getEnv(self):
        return self.env

    def addEnv(self, envName, envValue):
        self.env[envName] = envValue
