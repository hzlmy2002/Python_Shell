import sys

sys.path.insert(1, "../src")
from apps import tools
from apps import *
from Stream import *
import unittest, os
from standardStreamExceptions import *


class testApps(unittest.TestCase):
    def setUp(self) -> None:
        with open("testA.txt", "w") as file:
            file.write("testA\n")
        with open("testB.txt", "w") as file:
            file.write("testB")

    def tearDown(self) -> None:
        os.remove("testA.txt")
        os.remove("testB.txt")

    def testGrepFindPattern(self):
        stream = Stream(streamType.input, "grep", [], [], {})
        app = Grep()
        appUnsafe = GrepUnsafe()
        result1 = app.exec(stream)
        result2 = appUnsafe.exec(stream)

    def testGrepStdin(self):
        stream = Stream(
            streamType.input, "grep", [], [tools.str2stdin("Hello World!\n")], {}
        )
        app = Grep()
        appUnsafe = GrepUnsafe()
        result1 = app.exec(stream)
        result2 = appUnsafe.exec(stream)
        self.assertEqual(result1.args[0], result2.args[0])
        self.assertEqual(result1.args[0], "Hello World!\n")

    def testGrepExceptions(self):
        msg = stdExceptionMessage()
        """stream1 = Stream(streamType.input, "pwd", [], ["smh"], {})  # Contains argument
        stream2 = Stream(
            streamType.input, "pwd", [], ["smh", "smh"], {}
        )  # Contains arguments
        stream3 = Stream(streamType.input, "pwd", ["smh"], [], {})  # Contains parameter
        stream4 = Stream(
            streamType.input, "pwd", ["smh", "smh"], [], {}
        )  # Contains parameters
        stream5 = None
        app = Pwd()
        appUnsafe = PwdUnsafe()
        with self.assertRaises(Exception):
            app.exec(stream1)
        with self.assertRaises(Exception):
            app.exec(stream2)
        with self.assertRaises(Exception):
            app.exec(stream3)
        with self.assertRaises(Exception):
            app.exec(stream4)
        with self.assertRaises(Exception):
            app.exec(stream5)
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum) in appUnsafe.exec(stream1).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum) in appUnsafe.exec(stream2).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum) in appUnsafe.exec(stream3).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum) in appUnsafe.exec(stream4).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none) in appUnsafe.exec(stream5).args[0]
        )"""


if __name__ == "__main__":
    unittest.main(verbosity=2)
