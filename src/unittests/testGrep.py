import sys

sys.path.insert(0, "..")

from apps import *
import unittest, os
from apps.Exceptions import (
    InvalidArgumentError,
    InvalidParamError,
    InvalidFileOrDir,
    MissingParamError,
)
from appTests import appTests


class testGrep(unittest.TestCase):
    def setUp(self) -> None:
        with open("testA.txt", "w") as file:
            file.write("AAA\nBBB\nCCC")
        with open("testB.txt", "w") as file:
            file.write("BBB\nCCC\nDDD")
        with open("testC.txt", "w") as file:
            file.write("BBB\nCCC\nBBB")
        self.tester = appTests(grep)

    def tearDown(self) -> None:
        os.remove("testA.txt")
        os.remove("testB.txt")

    def findPatternHelper(self, result1, result2, stringPattern):
        self.assertEqual(result1, result2)
        self.assertEqual(result1, stringPattern)

    def testGrepFindPattern(self):
        # appUnsafe = GrepUnsafe()
        result1 = self.tester.doOuputTest(["AAA", "testA.txt"])
        # result2 = appUnsafe.exec(stream)
        result3 = self.tester.doOuputTest(["AAA", "testA.txt", "testB.txt"])
        # result4 = appUnsafe.exec(stream2)
        result5 = self.tester.doOuputTest(["BBB", "testA.txt", "testB.txt"])
        # result6 = appUnsafe.exec(stream3)
        result7 = self.tester.doOuputTest(["...", "testA.txt"])
        result9 = self.tester.doOuputTest(["B..", "testC.txt"])

        # TODO add unsafe
        self.findPatternHelper(result1, result1, "AAA\n")
        self.findPatternHelper(result3, result3, "testA.txt:AAA\n")
        self.findPatternHelper(result5, result5, "testA.txt:BBB\ntestB.txt:BBB\n")
        self.findPatternHelper(result7, result7, "AAA\nBBB\nCCC\n")
        self.findPatternHelper(result9, result9, "BBB\nBBB\n")

    def testGrepExceptions(self):
        # appUnsafe = GrepUnsafe()
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["testA.txt"])  # No pattern specified
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["pattern"])  # No file specified
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest(["AAA", "smh", "testA.txt"])  # Not existing file
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([])  # Empty
        """self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum)
            in appUnsafe.exec(stream1).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum)
            in appUnsafe.exec(stream2).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.tagNum)
            in appUnsafe.exec(stream3).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.file)
            in appUnsafe.exec(stream4).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none)
            in appUnsafe.exec(stream5).params["main"][0]
        )

        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum)
            in appUnsafe.exec(stream6).params["main"][0]
        )"""


if __name__ == "__main__":
    unittest.main(verbosity=2)
