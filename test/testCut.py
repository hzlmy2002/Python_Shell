import sys

sys.path.insert(0, "../src")
import os
import unittest
from appTests import appTests
from apps.Exceptions import (
    InvalidArgumentError,
    InvalidParamError,
    InvalidFileOrDir,
    MissingParamError,
)
from apps.Cut import cut
from appTests import appTests


class testCut(appTests):
    def setUp(self) -> None:
        with open("testA.txt", "w") as file:
            file.write(
                "Hello World, this is Cut test\n"
                + "My name is something\nNice to meet\nyou all"
            )
        self.setApp(cut, "cut")

    def tearDown(self) -> None:
        os.remove("testA.txt")

    def testCutFile(self):
        self.outputAssertHelper(["-b", "1,2", "testA.txt"])
        self.outputAssertHelper(["-b", "-2,5-", "testA.txt"])
        self.outputAssertHelper(["-b", "3-5", "testA.txt"])
        self.outputAssertHelper(
            ["-b", "4,3-5,-6", "testA.txt"]
        )  # Testing combining ranges
        self.outputAssertHelper(
            ["-b", "6-,3-5", "testA.txt"]
        )  # Testing unordered ranges
        self.outputAssertHelper(["-b", "1", "testA.txt"])
        self.outputAssertHelper(
            ["-b", "2-,3-5", "testA.txt"]
        )  # Testing unordered ranges

    def testCutExceptions(self):
        self.exceptionAssertHelper(
            ["testA.txt"], MissingParamError, "MissingParamError"
        )  # No param b specified
        self.exceptionAssertHelper(
            ["-b", "testA.txt"], InvalidArgumentError, "InvalidArgumentError"
        )  # No param arg specified
        self.exceptionAssertHelper(
            ["-b", "3-5", "smh.txt"], InvalidFileOrDir, "InvalidFileOrDir"
        )  # Not valid file specified
        self.exceptionAssertHelper(
            ["-b", "3-5", "testB.txt", "testA.txt"],
            InvalidArgumentError,
            "InvalidArgumentError",
        )  # Too many arguments
        self.exceptionAssertHelper(
            ["-b", "5-3", "testA.txt"], InvalidArgumentError, "InvalidArgumentError"
        )  # Decreasing range
        self.exceptionAssertHelper(
            ["-b", "n", "testA.txt"], InvalidParamError, "InvalidParamError"
        )  # Invalid param arg
        self.exceptionAssertHelper(
            ["-b", "1,3,", "testA.txt"], InvalidParamError, "InvalidParamError"
        )  # Invalid param arg (ends with comma)
        self.exceptionAssertHelper(
            ["-b", "1-2-3", "testA.txt"], InvalidParamError, "InvalidParamError"
        )  # Invalid param arg
        self.exceptionAssertHelper(
            ["-b", "1-3"], InvalidArgumentError, "InvalidArgumentError"
        )  # No file specified
        self.exceptionAssertHelper(
            ["-b", "1-3", ""], InvalidArgumentError, "InvalidArgumentError"
        )  # No file specified
        self.exceptionAssertHelper(
            [], InvalidArgumentError, "InvalidArgumentError"
        )  # Empty


if __name__ == "__main__":
    unittest.main(verbosity=2)
