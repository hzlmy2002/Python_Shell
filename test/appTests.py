from StdOutForTest import StdOutForTest
from StreamForTest import StreamForTest
from typing import Dict, List, Callable
from apps.decorators import unsafe


class appTests:
    def __init__(self, app: Callable[["StreamForTest"], None]) -> None:
        self.app = app

    def doOuputTest(
        self, arg: List[str] = [], env: Dict[str, str] = {}, unsafeApp=False
    ) -> str:
        stdOut = StdOutForTest()
        stream = StreamForTest(env, stdOut, arg)
        if unsafeApp:
            unsafeApp = unsafe(self.app)
            unsafeApp(stream)
        else:
            self.app(stream)
        result = stdOut.getOut()
        return result

    def changeEnvTest(
        self, arg: List[str] = [], env: Dict[str, str] = {}, unsafeApp=False
    ):
        stdOut = StdOutForTest()
        stream = StreamForTest(env, stdOut, arg)
        if unsafeApp:
            unsafeApp = unsafe(self.app)
            unsafeApp(stream)
        else:
            self.app(stream)
        return stream.getEnv("workingDir")
