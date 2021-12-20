import sys

sys.path.insert(0, "../src")
import os
import unittest
from appTests import appTests
from apps.exceptions import (
    InvalidArgumentError,
    InvalidFileOrDir,
    MissingStdin,
)
from apps.grep import grep


class testGrep(appTests):
    def setUp(self) -> None:
        with open("testA.txt", "w") as file:
            file.write("AAA\nBBB\nCCC")
        with open("testB.txt", "w") as file:
            file.write("BBB\nCCC\nDDD")
        with open("testC.txt", "w") as file:
            file.write("BBB\nCCC\nBBB")
        self.setApp(grep, "grep")

    def tearDown(self) -> None:
        os.remove("testA.txt")
        os.remove("testB.txt")
        os.remove("testC.txt")

    def testGrepFindPattern(self):
        self.outputAssertHelper(["AAA", "testA.txt"])
        self.outputAssertHelper(["AAA", "testA.txt", "testB.txt"])
        self.outputAssertHelper(["BBB", "testA.txt", "testB.txt"])
        self.outputAssertHelper(["...", "testA.txt"])
        self.outputAssertHelper(["B..", "testC.txt"])

    def testGrepExceptions(self):
        self.exceptionAssertHelper(
            ["testA.txt"], MissingStdin, "MissingStdin"
        )  # No pattern specified
        self.exceptionAssertHelper(
            ["pattern"], MissingStdin, "MissingStdin"
        )  # No file specified
        self.exceptionAssertHelper(
            ["AAA", "smh", "testA.txt"], InvalidFileOrDir, "InvalidFileOrDir"
        )  # Not existing file
        self.exceptionAssertHelper(
            [], InvalidArgumentError, "InvalidArgumentError"
        )  # Empty


if __name__ == "__main__":
    unittest.main(verbosity=2)
