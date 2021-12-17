from StdOutForTest import StdOutForTest
from StreamForTest import StreamForTest
from typing import List, Callable
from apps.decorators import unsafe
import unittest
import subprocess


class appTests(unittest.TestCase):
    def setApp(self, app: Callable[["StreamForTest"], None], name: str) -> None:
        self.app = app
        self.name = name

    def doOutputTest(
        self,
        arg: List[str],
        env: str = "",
        unsafeApp=False,
        getEnv=False,
    ) -> str:
        stdOut = StdOutForTest()
        stream = StreamForTest(env, stdOut, None, arg.copy())
        if unsafeApp:
            unsafeApp = unsafe(self.app)
            unsafeApp(stream)
        else:
            self.app(stream)
        if getEnv:
            result = stream.getWorkingDir()
        else:
            result = stdOut.getOut()
        return result

    def outputAssertHelper(self, arg: "List[str]" = [], env: str = "", ordered=True):
        # Helps asserting app output with actual bash output and unsafe app output
        result1 = self.doOutputTest(arg=arg, env=env)
        result2 = self.doOutputTest(arg=arg, env=env, unsafeApp=True)
        self.assertEqual(result1, result2)
        osRunCommand = subprocess.run([self.name] + arg, capture_output=True, text=True)
        returned = osRunCommand.stdout
        if ordered:
            self.assertEqual(result1.strip(), returned.strip())
        else:
            self.assertEqual(
                set(result1.strip().split("\n")), set(result2.strip().split("\n"))
            )

    def exceptionAssertHelper(self, arg: "List[str]", exception, strException):
        # Helps asserting exception is raised
        # And unsafe correspondence prints out exception
        with self.assertRaises(exception):
            self.doOutputTest(arg, env="")
        self.assertTrue(strException in self.doOutputTest(arg, env="", unsafeApp=True))
