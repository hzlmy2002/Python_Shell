from re import T
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
        os.remove("testC.txt")

    def findPatternHelper(self, result1, result2, stringPattern):
        self.assertEqual(result1, result2)
        self.assertEqual(result1, stringPattern)

    def testGrepFindPattern(self):
        result1 = self.tester.doOuputTest(["AAA", "testA.txt"])
        result2 = self.tester.doOuputTest(["AAA", "testA.txt"], unsafeApp=True)
        result3 = self.tester.doOuputTest(["AAA", "testA.txt", "testB.txt"])
        result4 = self.tester.doOuputTest(
            ["AAA", "testA.txt", "testB.txt"], unsafeApp=True
        )
        result5 = self.tester.doOuputTest(["BBB", "testA.txt", "testB.txt"])
        result6 = self.tester.doOuputTest(
            ["BBB", "testA.txt", "testB.txt"], unsafeApp=True
        )
        result7 = self.tester.doOuputTest(["...", "testA.txt"])
        result8 = self.tester.doOuputTest(["...", "testA.txt"], unsafeApp=True)
        result9 = self.tester.doOuputTest(["B..", "testC.txt"])
        result10 = self.tester.doOuputTest(["B..", "testC.txt"], unsafeApp=True)
        self.findPatternHelper(result1, result2, "AAA\n")
        self.findPatternHelper(result3, result4, "testA.txt:AAA\n")
        self.findPatternHelper(result5, result6, "testA.txt:BBB\ntestB.txt:BBB\n")
        self.findPatternHelper(result7, result8, "AAA\nBBB\nCCC\n")
        self.findPatternHelper(result9, result10, "BBB\nBBB\n")

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
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["testA.txt"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["pattern"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidFileOrDir"
            in self.tester.doOuputTest(["AAA", "smh", "testA.txt"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError" in self.tester.doOuputTest([], unsafeApp=True)
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
