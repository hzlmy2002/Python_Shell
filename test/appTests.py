from StdOutForTest import StdOutForTest
from StreamForTest import StreamForTest
from typing import List, Callable
from apps.decorators import unsafe


class appTests:
    def __init__(self, app: Callable[["StreamForTest"], None]) -> None:
        self.app = app

    def doOuputTest(
        self, arg: List[str] = [], env: str = "", unsafeApp=False, stdin=None
    ) -> str:
        stdOut = StdOutForTest()
        stream = StreamForTest(env, stdOut, stdin, arg)
        if unsafeApp:
            unsafeApp = unsafe(self.app)
            unsafeApp(stream)
        else:
            self.app(stream)
        result = stdOut.getOut()
        return result

    def changeEnvTest(
        self, arg: List[str] = [], env: str = "", unsafeApp=False, stdin=None
    ):
        stdOut = StdOutForTest()
        stream = StreamForTest(env, stdOut, stdin, arg)
        if unsafeApp:
            unsafeApp = unsafe(self.app)
            unsafeApp(stream)
        else:
            self.app(stream)
        return stream.getWorkingDir()
