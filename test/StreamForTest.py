from apps.Stream import Stream
from typing import Dict, List


class StreamForTest(Stream):
    def __init__(self, env: Dict[str, str], stdout, args: List[str] = []):
        super().__init__(env, stdout)
        self.args = args
