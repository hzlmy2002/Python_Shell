import sys

sys.path.insert(0, "../src")

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
        result1 = self.tester.doOuputTest(["-b", "1,2", "testA.txt"])
        result2 = self.tester.doOuputTest(["-b", "1,2", "testA.txt"], unsafeApp=True)
        result3 = self.tester.doOuputTest(["-b", "-2,5-", "testA.txt"])
        result4 = self.tester.doOuputTest(["-b", "-2,5-", "testA.txt"], unsafeApp=True)
        result5 = self.tester.doOuputTest(["-b", "3-5", "testA.txt"])
        result6 = self.tester.doOuputTest(["-b", "3-5", "testA.txt"], unsafeApp=True)
        result7 = self.tester.doOuputTest(
            ["-b", "4,3-5,-6", "testA.txt"]
        )  # Testing combining ranges
        result8 = self.tester.doOuputTest(
            ["-b", "4,3-5,-6", "testA.txt"], unsafeApp=True
        )
        result9 = self.tester.doOuputTest(
            ["-b", "6-,3-5", "testA.txt"]
        )  # Testing unordered ranges
        result10 = self.tester.doOuputTest(
            ["-b", "6-,3-5", "testA.txt"], unsafeApp=True
        )
        self.assertHelper(result1, result2, "He\nMy\nNi\nyo\n")
        self.assertHelper(
            result3,
            result4,
            "Heo World, this is Cut test\nMyame is something\nNi to meet\nyoall\n",
        )
        self.assertHelper(result5, result6, "llo\n na\nce \nu a\n")
        self.assertHelper(result7, result8, "Hello \nMy nam\nNice t\nyou al\n")
        self.assertHelper(
            result9,
            result10,
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
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["-b", "1-3", ""])  # No file specified
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([""])  # Empty
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([])  # Empty
        self.assertTrue(
            "MissingParamError"
            in self.tester.doOuputTest(["testA.txt"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["-b", "testA.txt"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidFileOrDir"
            in self.tester.doOuputTest(["-b", "3-5", "smh.txt"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(
                ["-b", "3-5", "testB.txt", "testA.txt"], unsafeApp=True
            )
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["-b", "5-3", "testA.txt"], unsafeApp=True)
        )

        self.assertTrue(
            "InvalidParamError"
            in self.tester.doOuputTest(["-b", "n", "testA.txt"], unsafeApp=True)
        )

        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["-b", "1-3"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["-b", "1-3", ""], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError" in self.tester.doOuputTest([""], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError" in self.tester.doOuputTest([], unsafeApp=True)
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
