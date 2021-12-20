import sys

sys.path.insert(0, "../src")
import os
import unittest
from appTests import appTests
from apps.exceptions import (
    InvalidArgumentError,
    InvalidParamError,
    InvalidFileOrDir,
    MissingParamError,
    MissingStdin,
)
from apps.cut import cut
from hypothesis import given, assume, example, strategies as st
import re


def isDecreaseRange(bRange: str):
    if len(bRange) == 3:
        return bRange[2] < bRange[0]
    return False


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

    @given(
        s1=st.from_regex(re.compile("([1-9]-[1-9]?|[1-9]?-[1-9])"), fullmatch=True),
        s2=st.from_regex(re.compile("([1-9]-[1-9]?|[1-9]?-[1-9])"), fullmatch=True),
        s3=st.from_regex(re.compile("([1-9]-[1-9]?|[1-9]?-[1-9])"), fullmatch=True),
    )
    @example(s1="4", s2="3-5", s3="-6")  # Testing combining ranges
    @example(s1="6-", s2="3-5", s3="")  # Testing unordered ranges
    @example(s1="2-", s2="3-5", s3="")  # Testing unordered ranges
    def testCutFile(self, s1: str, s2: str, s3: str):
        assume(
            not isDecreaseRange(s1)
            and not isDecreaseRange(s2)
            and not isDecreaseRange(s3)
        )
        bRange = ",".join(list(filter(lambda x: x != "", [s1, s2, s3])))
        self.outputAssertHelper(["-b", bRange, "testA.txt"])

    def testCutExceptions(self):
        self.exceptionAssertHelper(
            ["testA.txt"], MissingParamError, "MissingParamError"
        )  # No param b specified
        self.exceptionAssertHelper(
            ["-b", "testA.txt"], MissingStdin, "MissingStdin"
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
            ["-b", "1-3"], MissingStdin, "MissingStdin"
        )  # No file specified
        self.exceptionAssertHelper(
            ["-b", "1-3", ""], InvalidArgumentError, "InvalidArgumentError"
        )  # No file specified
        self.exceptionAssertHelper(
            [], InvalidArgumentError, "InvalidArgumentError"
        )  # Empty


if __name__ == "__main__":
    unittest.main(verbosity=2)
