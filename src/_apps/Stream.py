from typing import List, Dict

from enum import Enum


class streamType(Enum):
    input = 0
    output = 1
    error = -1


class Stream:
    def __init__(
        self,
        sType: streamType,
        app: str,
        params: Dict[str, str],
        env: Dict[str, str],
    ) -> None:
        """
        self.stream_type (int) : 0 represents input, 1 represents output, -1 represents error
        self.app (String)
        self.param (List of String)
        self.args (List of String)
        """
        self.sType = sType
        self.app = app
        self.params = params.copy()
        if "main" not in self.params:
            self.params["main"] = []
        self.env = env.copy()

    def getApp(self):
        return self.app

    def getParams(self):
        return self.params.copy()

    def getEnv(self):
        return self.env

    def addEnv(self, envName, envValue):
        self.env[envName] = envValue

    def __repr__(self):
        return f"<Stream Object> stype: {self.sType} | app: {self.app} | params: {self.params} | env: {self.env}"
