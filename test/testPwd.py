import sys

sys.path.insert(0, "../src")
import os
import unittest
from appTests import appTests
from apps.pwd import pwd


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


if __name__ == "__main__":
    unittest.main(verbosity=2)
