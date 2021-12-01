from StdOutForTest import StdOutForTest
from StreamForTest import StreamForTest
from typing import Dict, List, Callable


class appTests:
    def __init__(self, app: Callable[["StreamForTest"], None]) -> None:
        self.app = app

    def doOuputTest(
        self,
        arg: List[str] = [],
        env: Dict[str, str] = {},
    ) -> str:
        stdOut = StdOutForTest()
        stream = StreamForTest(env, stdOut, arg)
        self.app(stream)
        result = stdOut.getOut()
        return result
