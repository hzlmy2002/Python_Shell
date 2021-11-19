import sys

sys.path.insert(0, "..")
from apps import tools
from apps import *
from Stream import *
import unittest, os


class testApps(unittest.TestCase):
    def setUp(self) -> None:
        with open("testA.txt", "w") as file:
            file.write("AAA\nBBB\nCCC")
        with open("testB.txt", "w") as file:
            file.write("BBB\nCCC\nDDD")

    def tearDown(self) -> None:
        os.remove("testA.txt")
        os.remove("testB.txt")

    def findPatternHelper(self, result1, result2, stringPattern):
        self.assertEqual(result1.getArgs(), result2.getArgs())
        self.assertEqual(result1.getArgs()[0], stringPattern)

    def testGrepFindPattern(self):
        stream = Stream(streamType.input, "grep", ["AAA"], ["testA.txt"], {})
        stream2 = Stream(
            streamType.input, "grep", ["AAA"], ["testA.txt", "testB.txt"], {}
        )
        stream3 = Stream(
            streamType.input, "grep", ["BBB"], ["testA.txt", "testB.txt"], {}
        )
        app = Grep()
        appUnsafe = GrepUnsafe()
        result1 = app.exec(stream)
        result2 = appUnsafe.exec(stream)
        result3 = app.exec(stream2)
        result4 = appUnsafe.exec(stream2)
        result5 = app.exec(stream3)
        result6 = appUnsafe.exec(stream3)
        self.findPatternHelper(result1, result2, "AAA\n")
        self.findPatternHelper(result3, result4, "testA.txt:AAA\n")
        self.findPatternHelper(result5, result6, "testA.txt:BBB\ntestB.txt:BBB\n")

    def testGrepStdin(self):
        stream = Stream(
            streamType.input,
            "grep",
            ["pattern"],
            [tools.str2stdin("Hello World!\n")],
            {},
        )
        app = Grep()
        appUnsafe = GrepUnsafe()
        result1 = app.exec(stream)
        result2 = appUnsafe.exec(stream)
        self.assertEqual(result1.args[0], result2.args[0])
        self.assertEqual(result1.args[0], "Hello World!\n")

    def testGrepExceptions(self):
        msg = stdExceptionMessage()
        stream1 = Stream(
            streamType.input, "grep", [], ["testA.txt"], {}
        )  # No Pattern specified
        stream2 = Stream(
            streamType.input, "grep", ["pattern"], [], {}
        )  # No File specified
        stream3 = Stream(
            streamType.input, "pwd", ["AAA", "BBB"], ["test.txt"], {}
        )  # Multiple patterns specified
        stream4 = Stream(
            streamType.input, "pwd", ["AAA"], ["smh"], {}
        )  # Invalid File specified
        stream5 = None
        app = Grep()
        appUnsafe = GrepUnsafe()
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
            msg.exceptionMsg(exceptionType.paramNum) in appUnsafe.exec(stream1).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum) in appUnsafe.exec(stream2).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum) in appUnsafe.exec(stream3).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.file) in appUnsafe.exec(stream4).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none) in appUnsafe.exec(stream5).args[0]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
