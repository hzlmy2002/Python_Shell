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
            file.write("l1\nl2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\nl12\n")

    def tearDown(self) -> None:
        os.remove("test.txt")

    def testTailFile(self):
        stream1 = Stream(streamType.input, "tail", [], ["test.txt"], {})
        stream2 = Stream(streamType.input, "tail", ["-n"], [11, "test.txt"], {})
        tail = Tail()
        tailUnsafe = TailUnsafe()
        result1 = tail.exec(stream1)
        result2 = tailUnsafe.exec(stream1)
        result3 = tail.exec(stream2)
        result4 = tailUnsafe.exec(stream2)
        self.assertEqual(result1.getArgs()[0], result2.getArgs()[0])
        self.assertEqual(
            result1.getArgs()[0], "l3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\nl12\n"
        )
        self.assertEqual(result3.getArgs()[0], result4.getArgs()[0])
        self.assertEqual(
            result3.getArgs()[0], "l2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\nl12\n"
        )

    def testTailStdin(self):
        stream = Stream(
            streamType.input, "tail", [], [tools.str2stdin("Hello World!\n")], {}
        )
        tail = Tail()
        tailUnsafe = TailUnsafe()
        """result1 = head.exec(stream)
        result2 = headUnsafe.exec(stream)
        self.assertEqual(result1.args[0], result2.args[0])
        self.assertEqual(result1.args[0], "Hello World!\n")"""

    def testTailExceptions(self):
        msg = stdExceptionMessage()
        stream1 = Stream(streamType.input, "tail", [], [], {})  # No param no arg
        stream2 = Stream(streamType.input, "tail", ["a"], [], {})  # Param with no arg
        stream3 = Stream(
            streamType.input, "tail", [], [11, "test.txt"], {}
        )  # Two arg with no param
        stream4 = Stream(
            streamType.input, "tail", ["smh"], [11, "test.txt"], {}
        )  # Invalid param tag
        stream5 = Stream(streamType.input, "tail", [], ["smh"], {})  # Not existing file
        stream6 = None
        tail = Tail()
        tailUnsafe = TailUnsafe()
        with self.assertRaises(Exception):
            tail.exec(stream1)
        with self.assertRaises(Exception):
            tail.exec(stream2)
        with self.assertRaises(Exception):
            tail.exec(stream3)
        with self.assertRaises(Exception):
            tail.exec(stream4)
        with self.assertRaises(Exception):
            tail.exec(stream5)
        with self.assertRaises(Exception):
            tail.exec(stream6)
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum) in tailUnsafe.exec(stream1).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum) in tailUnsafe.exec(stream2).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum) in tailUnsafe.exec(stream3).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramType)
            in tailUnsafe.exec(stream4).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.file) in tailUnsafe.exec(stream5).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none) in tailUnsafe.exec(stream6).args[0]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
