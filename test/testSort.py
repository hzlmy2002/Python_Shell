import sys

sys.path.insert(0, "../src")
import os
import unittest
from appTests import appTests
from apps.Exceptions import (
    InvalidArgumentError,
    InvalidFileOrDir,
    InvalidParamTagError,
    MissingStdin,
)
from apps.Sort import sort


class testSort(appTests):
    def setUp(self) -> None:
        with open("testA.txt", "w") as file:
            file.write(
                "Two roads diverged in a yello wood,\n"
                + "And sorry I could not travel both\n"
                + "And be one traveler,long I stood\n"
                + "And looked down one as far as I could\n"
                + "To where it bent in the undergrowth"
            )
        self.setApp(sort, "sort")

    def tearDown(self) -> None:
        os.remove("testA.txt")

    def testSortFile(self):
        self.outputAssertHelper(["testA.txt"])
        self.outputAssertHelper(["-r", "testA.txt"])

    def testSortExceptions(self):
        self.exceptionAssertHelper(
            ["testB.txt", "testA.txt"], InvalidArgumentError, "InvalidArgumentError"
        )  # Too many arguments
        self.exceptionAssertHelper(
            [], MissingStdin, "MissingStdin"
        )  # Empty argument without stdin
        self.exceptionAssertHelper(
            ["-r"], MissingStdin, "MissingStdin"
        )  # Empty argument without stdin
        self.exceptionAssertHelper(
            ["-r", "123", "testA.txt"], InvalidArgumentError, "InvalidArgumentError"
        )  # Too many arguments
        self.exceptionAssertHelper(
            ["-r", "smh"], InvalidFileOrDir, "InvalidFileOrDir"
        )  # Not existing file
        self.exceptionAssertHelper(
            ["-a", "testA.txt"], InvalidParamTagError, "InvalidParamTagError"
        )  # Invalid flag A


if __name__ == "__main__":
    unittest.main(verbosity=2)
