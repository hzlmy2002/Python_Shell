import sys

sys.path.insert(0, "..")

from apps import *
from apps.Stream import *
import unittest


class testApps(unittest.TestCase):
    def testEchoOutput(self):
        stream1 = Stream(streamType.input, "echo", {"main": ["testOut"]}, {})
        stream2 = Stream(
            streamType.input, "echo", {"main": ["testOut", "testOut2"]}, {}
        )
        echo = Echo()
        echoUnsafe = EchoUnsafe()
        result1 = echo.exec(stream1)
        result2 = echoUnsafe.exec(stream1)
        result3 = echo.exec(stream2)
        result4 = echo.exec(stream2)
        self.assertEqual(result1.params["main"][0], "testOut\n")
        self.assertEqual(result1.params["main"][0], result2.params["main"][0])
        self.assertEqual(result3.params["main"][0], "testOut testOut2\n")
        self.assertEqual(result3.params["main"][0], result4.params["main"][0])

    def testEchoExceptions(self):
        msg = stdExceptionMessage()
        stream1 = Stream(
            streamType.input, "echo", {"a": ["a"], "main": ["testDir"]}, {}
        )  # Has param case
        stream2 = Stream(streamType.input, "echo", {"main": []}, {})  # No args case
        stream3 = None
        echo = Echo()
        echoUnsafe = EchoUnsafe()
        with self.assertRaises(Exception):
            echo.exec(stream1)
        with self.assertRaises(Exception):
            echo.exec(stream2)
        with self.assertRaises(Exception):
            echo.exec(stream3)
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum)
            in echoUnsafe.exec(stream1).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum)
            in echoUnsafe.exec(stream2).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none)
            in echoUnsafe.exec(stream3).params["main"][0]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
