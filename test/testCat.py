import sys

sys.path.insert(0, "../src")
import os
import unittest
from apps.Exceptions import InvalidFileOrDir, MissingStdin
from appTests import appTests
from apps.Cat import cat


class testCat(appTests):
    def setUp(self) -> None:
        with open(".testCatA.txt", "w") as file:
            file.write("TestLineA\nTestLineAA\n")
        with open(".testCatB.txt", "w") as file:
            file.write("testCatB")
        self.setApp(cat, "cat")

    def tearDown(self) -> None:
        os.remove(".testCatA.txt")
        os.remove(".testCatB.txt")

    def testCatFile(self):
        self.outputAssertHelper([".testCatA.txt", ".testCatB.txt"])

    def testCatExceptions(self):
        self.exceptionAssertHelper(
            ["^^^"], InvalidFileOrDir, "InvalidFileOrDir"
        )  # Not existing file
        self.exceptionAssertHelper([], MissingStdin, "MissingStdin")  # No argument
        self.exceptionAssertHelper(
            [""], InvalidFileOrDir, "InvalidFileOrDir"
        )  # No argument


if __name__ == "__main__":
    unittest.main(verbosity=2)
