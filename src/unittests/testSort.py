import sys

sys.path.insert(0, "..")

from apps import *
import unittest, os
from apps.Exceptions import (
    InvalidArgumentError,
    InvalidParamError,
    InvalidFileOrDir,
    MissingParamError,
    InvalidParamTagError,
)
from appTests import appTests


class testSort(unittest.TestCase):
    def setUp(self) -> None:
        with open("testA.txt", "w") as file:
            file.write(
                "Two roads diverged in a yello wood,\nAnd sorry I could not travel both\nAnd be one traveler,long I stood\nAnd looked down one as far as I could\nTo where it bent in the undergrowth"
            )
        self.tester = appTests(sort)

    def tearDown(self) -> None:
        os.remove("testA.txt")

    def matchHelper(self, result1, result2, stringPattern):
        self.assertEqual(result1, result2)
        self.assertEqual(result1, stringPattern)

    def testSortFile(self):
        # appUnsafe = SortUnsafe()
        result1 = self.tester.doOuputTest(["testA.txt"])
        # result2 = appUnsafe.exec(stream)
        result3 = self.tester.doOuputTest(["-r", "testA.txt"])
        # result4 = appUnsafe.exec(stream2)
        answer = [
            "And be one traveler,long I stood\n",
            "And looked down one as far as I could\n",
            "And sorry I could not travel both\n",
            "To where it bent in the undergrowth\n",
            "Two roads diverged in a yello wood,\n",
        ]

        # Add unsafe later
        self.matchHelper(
            result1,
            result1,
            "".join(answer),
        )
        self.matchHelper(result3, result3, "".join(answer[::-1]))

    def testSortExceptions(self):
        # appUnsafe = SortUnsafe()
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["testB.txt", "testA.txt"])  # Too many arguments
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([])  # Empty argument
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["-r", "123", "testA.txt"])  # Too many arguments
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest(["-r", "smh"])  # Not existing file
        with self.assertRaises(InvalidParamTagError):
            self.tester.doOuputTest(["-a", "testA.txt"])  # Invalid flag A
        """
        self.assertTrue(
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
            msg.exceptionMsg(exceptionType.paramType)
            in appUnsafe.exec(stream6).params["main"][0]
        )"""


if __name__ == "__main__":
    unittest.main(verbosity=2)
