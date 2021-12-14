from apps.Stream import Stream
from typing import List


class StreamForTest(Stream):
    def __init__(self, env: str, stdout, stdin, args: List[str] = []):
        super().__init__(env)
        self.stdout = stdout
        self.stdin = stdin
        self.args = args
