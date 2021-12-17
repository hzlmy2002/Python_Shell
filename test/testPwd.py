import sys

sys.path.insert(0, "../src")
import os
import unittest
from apps.Exceptions import InvalidArgumentError
from appTests import appTests
from apps.Pwd import pwd
from appTests import appTests


class testPwd(appTests):
    def setUp(self) -> None:
        os.mkdir("testDir")
        self.cwd = os.getcwd()
        self.setApp(pwd, "pwd")

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        os.rmdir("testDir")

    def testPwdChangeDir(self):
        self.outputAssertHelper(env=self.cwd)

    def testPwdExceptions(self):
        self.exceptionAssertHelper(
            ["some args"], InvalidArgumentError, "InvalidArgumentError"
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
