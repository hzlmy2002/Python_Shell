import sys

sys.path.insert(0, "..")
from apps import *
from apps.Stream import *
from apps import tools
import unittest, os


class testApps(unittest.TestCase):
    def setUp(self) -> None:
        with open("test.txt", "w") as file:
            file.write("l1\nl2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\nl12\n")

    def tearDown(self) -> None:
        os.remove("test.txt")

    def testTailFile(self):
        stream1 = Stream(streamType.input, "tail", {"main": ["test.txt"]}, {})
        stream2 = Stream(
            streamType.input, "tail", {"n": [11], "main": ["test.txt"]}, {}
        )
        tail = Tail()
        tailUnsafe = TailUnsafe()
        result1 = tail.exec(stream1)
        result2 = tailUnsafe.exec(stream1)
        result3 = tail.exec(stream2)
        result4 = tailUnsafe.exec(stream2)
        self.assertEqual(result1.params["main"][0], result2.params["main"][0])
        self.assertEqual(
            result1.params["main"][0], "l3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\nl12\n"
        )
        self.assertEqual(result3.params["main"][0], result4.params["main"][0])
        self.assertEqual(
            result3.params["main"][0], "l2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\nl12\n"
        )

    def testTailStdin(self):
        stream = Stream(
            streamType.input,
            "tail",
            {"n": [], "main": [tools.str2stdin("Hello World!\n")]},
            {},
        )
        app = Tail()
        appUnsafe = TailUnsafe()
        result1 = app.exec(stream)
        result2 = appUnsafe.exec(stream)
        self.assertEqual(result1.params["main"], result2.params["main"])
        self.assertEqual(result1.params["main"][0], "Hello World!\n")

    def testTailExceptions(self):
        msg = stdExceptionMessage()
        stream1 = Stream(
            streamType.input, "head", {"n": [11], "main": []}, {}
        )  # Empty main arg
        stream2 = Stream(
            streamType.input, "head", {"a": [11], "main": ["test.txt"]}, {}
        )  # Invalid option a, only accepts n
        stream3 = Stream(
            streamType.input, "head", {"n": [11], "main": ["test.txt", "smh"]}, {}
        )  # Too many main arguments
        stream4 = Stream(
            streamType.input, "head", {"n": [11], "main": ["test.txt"], "a": [12]}, {}
        )  # Too many options provided
        stream5 = Stream(
            streamType.input, "head", {"n": [], "main": ["smh"]}, {}
        )  # Not existing file
        stream6 = None

        stream7 = Stream(
            streamType.input, "head", {"n": [], "main": ["test.txt"]}, {}
        )  # Empty n tag

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
            msg.exceptionMsg(exceptionType.argNum)
            in tailUnsafe.exec(stream1).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramType)
            in tailUnsafe.exec(stream2).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum)
            in tailUnsafe.exec(stream3).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum)
            in tailUnsafe.exec(stream4).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.file)
            in tailUnsafe.exec(stream5).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none)
            in tailUnsafe.exec(stream6).params["main"][0]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
