import sys

sys.path.insert(0, "../src")
import os
import unittest
from appTests import appTests
from apps.Exceptions import (
    InvalidArgumentError,
    InvalidParamTagError,
    InvalidFileOrDir,
    MissingStdin,
    InvalidParamError,
)
from apps.Head import head
from appTests import appTests


class testHead(appTests):
    def setUp(self) -> None:
        with open("test.txt", "w") as file:
            file.write("l1\nl2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\n")
        self.setApp(head, "head")

    def tearDown(self) -> None:
        os.remove("test.txt")

    def testHeadFile(self):
        self.outputAssertHelper(["test.txt"])
        self.outputAssertHelper(["-n", "11", "test.txt"])

    def testHeadExceptions(self):
        self.exceptionAssertHelper(
            ["-a", "11", "test.txt"], InvalidParamTagError, "InvalidParamTagError"
        )  # Invalid param tag -a
        self.exceptionAssertHelper(
            ["-n", "11", "smh", "test.txt"],
            InvalidArgumentError,
            "InvalidArgumentError",
        )  # Way to many arguments
        self.exceptionAssertHelper(
            ["-n", "11", "smh.txt"], InvalidFileOrDir, "InvalidFileOrDir"
        )  # Not existing file
        self.exceptionAssertHelper(
            ["-n", "11"], MissingStdin, "MissingStdin"
        )  # No stdin specified
        self.exceptionAssertHelper(
            ["-n", "test.txt"], InvalidParamError, "InvalidParamError"
        )  # No param argument specified or not valid parameter argument "test.txt"
        self.exceptionAssertHelper(
            [], MissingStdin, "MissingStdin"
        )  # No stdin specified


if __name__ == "__main__":
    unittest.main(verbosity=2)
