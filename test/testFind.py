import sys

sys.path.insert(0, "../src")
import os
import unittest
import shutil
from appTests import appTests
from apps.Exceptions import (
    InvalidArgumentError,
    InvalidFileOrDir,
    MissingParamError,
)
from apps.Find import find
from appTests import appTests


class testFind(appTests):
    def setUp(self) -> None:
        os.makedirs("root/testDir/test1")
        os.mkdir("root/testDir2/")
        f1 = open("root/test1.txt", "a")
        f1.close()
        f2 = open("root/testDir/test2.txt", "a")
        f2.close()
        f3 = open("root/testDir/Alttest1.txt", "a")
        f3.close()
        f4 = open("root/testDir/test1/test3.txt", "a")
        f4.close()
        f5 = open("root/testDir2/test4.txt", "a")
        f5.close()
        self.setApp(find, "find")

    def tearDown(self) -> None:
        shutil.rmtree("root")

    def testFindListFile(self):
        self.outputAssertHelper(["root", "-name", "test*.txt"], ordered=False)
        self.outputAssertHelper(["root", "-name", "Alt*.txt"], ordered=False)
        self.outputAssertHelper(["-name", "test*.txt"], ordered=False)

    def testFindExceptions(self):
        self.exceptionAssertHelper(
            ["root", "testDir2", "-name", "somepattern"],
            InvalidArgumentError,
            "InvalidArgumentError",
        )  # Too many arguments
        self.exceptionAssertHelper(
            ["root", "testDir2", "something", "somepattern"],
            MissingParamError,
            "MissingParamError",
        )  # No -name tag
        self.exceptionAssertHelper(
            ["smh", "-name", "somepattern"], InvalidFileOrDir, "InvalidFileOrDir"
        )  # Not existing path smh
        self.exceptionAssertHelper(
            ["root", "-name", "somepattern", "somemorepattern"],
            InvalidArgumentError,
            "InvalidArgumentError",
        )  # Too many patterns (too many arguments)
        self.exceptionAssertHelper(
            [], InvalidArgumentError, "InvalidArgumentError"
        )  # Empty


if __name__ == "__main__":
    unittest.main(verbosity=2)
