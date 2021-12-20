import sys

sys.path.insert(0, "../src")
import os
import unittest
from appTests import appTests
from apps.exceptions import (
    InvalidArgumentError,
    InvalidParamTagError,
    InvalidFileOrDir,
    MissingStdin,
)
from apps.uniq import uniq


class testUniq(appTests):
    def setUp(self) -> None:
        with open("testA.txt", "w") as file:
            file.write(
                "Hello Hello\nHELLO HELLO\nHello World\n"
                + "HelloHello\nHelloHello\nHelloHello\nWorld\nWorld\nWorld\n"
            )
        self.setApp(uniq, "uniq")

    def tearDown(self) -> None:
        os.remove("testA.txt")

    def testUniqFile(self):
        self.outputAssertHelper(["testA.txt"])
        self.outputAssertHelper(["-i", "testA.txt"])

    def testUniqExceptions(self):
        self.exceptionAssertHelper(
            ["smt", "testA.txt"], InvalidArgumentError, "InvalidArgumentError"
        )  # Too many arguments
        self.exceptionAssertHelper(
            [], MissingStdin, "MissingStdin"
        )  # No stdin specified
        self.exceptionAssertHelper(
            ["-i", "123", "testA.txt"], InvalidArgumentError, "InvalidArgumentError"
        )  # Too many arguments
        self.exceptionAssertHelper(
            ["-i", "smh"], InvalidFileOrDir, "InvalidFileOrDir"
        )  # Not existing file
        self.exceptionAssertHelper(
            ["-a", "testA.txt"], InvalidParamTagError, "InvalidParamTagError"
        )  # Invalid flag A


if __name__ == "__main__":
    unittest.main(verbosity=2)
