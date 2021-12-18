import sys

sys.path.insert(0, "../src")
import os
import unittest
import shutil
from appTests import appTests
from apps.Exceptions import InvalidArgumentError, InvalidFileOrDir
from apps.Ls import ls


class testLs(appTests):
    def setUp(self) -> None:
        self.cwd = os.getcwd()
        parent = "testDir/"
        os.makedirs(parent + "test1")
        os.makedirs(parent + "test2")
        os.makedirs(parent + ".test3")
        os.mkdir("testDir2")
        self.setApp(ls, "ls")

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        shutil.rmtree("testDir")
        shutil.rmtree("testDir2")

    def testLsListDir(self):
        self.outputAssertHelper(["testDir"])
        os.chdir("testDir")
        self.outputAssertHelper(env=os.getcwd())

    def testLsExceptions(self):
        self.exceptionAssertHelper(
            ["testDir", "testDir2"], InvalidArgumentError, "InvalidArgumentError"
        )  # Too many arguments
        self.exceptionAssertHelper(
            ["smh"], InvalidFileOrDir, "InvalidFileOrDir"
        )  # Not existing directory


if __name__ == "__main__":
    unittest.main(verbosity=2)
