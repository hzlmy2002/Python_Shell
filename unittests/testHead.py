import sys

sys.path.insert(1, "../src")
from standardStreamExceptions import *

sys.path.insert(1, "../src")

from apps import *
from Stream import *
from apps import tools
import unittest, os


class testApps(unittest.TestCase):
    def setUp(self) -> None:
        with open("test.txt", "w") as file:
            file.write("l1\nl2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\n")

    def tearDown(self) -> None:
        os.remove("test.txt")

    def testHeadFile(self):
        stream1 = Stream(streamType.input, "head", [], ["test.txt"], {})
        stream2 = Stream(streamType.input, "head", ["-n"], [11, "test.txt"], {})
        head = Head()
        headUnsafe = HeadUnsafe()
        result1 = head.exec(stream1)
        result2 = headUnsafe.exec(stream1)
        result3 = head.exec(stream2)
        result4 = headUnsafe.exec(stream2)
        self.assertEqual(result1.getArgs()[0], result2.getArgs()[0])
        self.assertEqual(
            result1.getArgs()[0], "l1\nl2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\n"
        )
        self.assertEqual(result3.getArgs()[0], result4.getArgs()[0])
        self.assertEqual(
            result3.getArgs()[0], "l1\nl2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\n"
        )

    def testHeadStdin(self):
        stream = Stream(
            streamType.input, "head", [], [tools.str2stdin("Hello World!\n")], {}
        )
        head = Head()
        headUnsafe = HeadUnsafe()
        """result1 = head.exec(stream)
        result2 = headUnsafe.exec(stream)
        self.assertEqual(result1.args[0], result2.args[0])
        self.assertEqual(result1.args[0], "Hello World!\n")"""

    def testHeadExceptions(self):
        msg = stdExceptionMessage()
        stream1 = Stream(streamType.input, "head", [], [], {})  # No param no arg
        stream2 = Stream(streamType.input, "head", ["a"], [], {})  # Param with no arg
        stream3 = Stream(
            streamType.input, "head", [], [11, "test.txt"], {}
        )  # Two arg with no param
        stream4 = Stream(
            streamType.input, "head", ["smh"], [11, "test.txt"], {}
        )  # Invalid param tag
        stream5 = Stream(streamType.input, "head", [], ["smh"], {})  # Not existing file
        stream6 = None
        head = Head()
        headUnsafe = HeadUnsafe()
        with self.assertRaises(Exception):
            head.exec(stream1)
        with self.assertRaises(Exception):
            head.exec(stream2)
        with self.assertRaises(Exception):
            head.exec(stream3)
        with self.assertRaises(Exception):
            head.exec(stream4)
        with self.assertRaises(Exception):
            head.exec(stream5)
        with self.assertRaises(Exception):
            head.exec(stream6)
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum) in headUnsafe.exec(stream1).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum) in headUnsafe.exec(stream2).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum) in headUnsafe.exec(stream3).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramType)
            in headUnsafe.exec(stream4).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.file) in headUnsafe.exec(stream5).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none) in headUnsafe.exec(stream6).args[0]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
