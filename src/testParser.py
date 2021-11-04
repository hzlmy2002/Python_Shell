import re
from glob import glob
from Stream import Stream


# Test Class for testing and standardizing streams and apps


class Parser:
    def __init__(self) -> None:
        self.dummy_file = "test.txt"
        self.dummy_file2 = "test2.txt"
        self.dummy_map = {
            "grep": ["grep", ["Hello"], [self.dummy_file]],
            "grep2": ["grep", ["Hello"], [self.dummy_file, self.dummy_file2]],
            "ls": ["ls", [], []],
            "cat": ["cat", [], [self.dummy_file]],
            "cat2": ["cat", [], [self.dummy_file, self.dummy_file2]],
            "cd": ["cd", [], [".."]],
            "echo": ["echo", [], ["Hello"]],
            "head": ["head", ["-n"], ["2", self.dummy_file]],
            "head2": ["head", [], [self.dummy_file]],
            "tail": ["tail", ["-n"], ["2", self.dummy_file]],
            "tail2": ["tail", [], [self.dummy_file]],
            "ls": ["ls", [], ["doc"]],
            "ls2": ["ls", [], []],
            "pwd": ["pwd", [], []],
        }

    def setup_stream(self, tokens):
        # Current setup includes the parameters into arguments
        application = tokens[0]
        param = tokens[1]
        arguments = tokens[2]
        return Stream(1, application, param, arguments, None)

    def parse(self, sing_com):
        # Packs input singular command into an stream object
        tokens = self.dummy_map[sing_com]
        return self.setup_stream(tokens)
