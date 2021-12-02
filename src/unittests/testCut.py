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


class testCut(unittest.TestCase):
    def setUp(self) -> None:
        with open("testA.txt", "w") as file:
            file.write(
                "Hello World, this is Cut test\nMy name is something\nNice to meet\nyou all"
            )
        self.tester = appTests(cut)

    def tearDown(self) -> None:
        os.remove("testA.txt")

    def assertHelper(self, result1, result2, stringPattern):
        self.assertEqual(result1, result2)
        self.assertEqual(result1, stringPattern)

    def testCutFile(self):
        # appUnsafe = CutUnsafe()
        result1 = self.tester.doOuputTest(["-b", "1,2", "testA.txt"])
        # result2 = appUnsafe.exec(stream)
        result3 = self.tester.doOuputTest(["-b", "-2,5-", "testA.txt"])
        # result4 = appUnsafe.exec(stream2)
        result5 = self.tester.doOuputTest(["-b", "3-5", "testA.txt"])
        # result6 = appUnsafe.exec(stream3)
        result7 = self.tester.doOuputTest(
            ["-b", "4,3-5,-6", "testA.txt"]
        )  # Testing combining ranges
        # result8 = appUnsafe.exec(stream4)
        result9 = self.tester.doOuputTest(
            ["-b", "6-,3-5", "testA.txt"]
        )  # Testing unordered ranges
        # result10 = appUnsafe.exec(stream5)

        # TODO replace second arg with unsafe
        self.assertHelper(result1, result1, "He\nMy\nNi\nyo\n")
        self.assertHelper(
            result3,
            result3,
            "Heo World, this is Cut test\nMyame is something\nNi to meet\nyoall\n",
        )
        self.assertHelper(result5, result5, "llo\n na\nce \nu a\n")
        self.assertHelper(result7, result7, "Hello \nMy nam\nNice t\nyou al\n")
        self.assertHelper(
            result9,
            result9,
            "llo World, this is Cut test\n name is something\nce to meet\nu all\n",
        )

    def testCutExceptions(self):
        # appUnsafe = CutUnsafe()
        with self.assertRaises(MissingParamError):
            self.tester.doOuputTest(["testA.txt"])  # No param b specified
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["-b", "testA.txt"])  # No param arg specified
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest(
                ["-b", "3-5", "smh.txt"]
            )  # Not valid file specified
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(
                ["-b", "3-5", "testB.txt", "testA.txt"]
            )  # Too many arguments
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["-b", "5-3", "testA.txt"])  # Decreasing range
        with self.assertRaises(InvalidParamError):
            self.tester.doOuputTest(["-b", "n", "testA.txt"])  # Invalid param arg
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["-b", "1-3"])  # No file specified
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
        )

        self.assertTrue(
            msg.exceptionMsg(exceptionType.decRange)
            in appUnsafe.exec(stream7).params["main"][0]
        )

        self.assertTrue(
            msg.exceptionMsg(exceptionType.tagType)
            in appUnsafe.exec(stream8).params["main"][0]
        )

        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum)
            in appUnsafe.exec(stream9).params["main"][0]
        )"""


if __name__ == "__main__":
    unittest.main(verbosity=2)
