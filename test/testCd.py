import sys

sys.path.insert(0, "../src")
import os
import unittest
from appTests import appTests
from apps.Exceptions import InvalidArgumentError, InvalidFileOrDir
from apps.Cd import cd


class testCd(appTests):
    def setUp(self) -> None:
        os.mkdir("testDir")
        self.cwd = os.getcwd()
        self.setApp(cd, "cd")

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        os.rmdir("testDir")

    def testCdChangeDir(self):
        result1 = self.doOutputTest(["testDir"], env=self.cwd, getEnv=True)
        os.chdir(self.cwd)
        result3 = self.doOutputTest(
            ["testDir"], env=self.cwd, unsafeApp=True, getEnv=True
        )
        self.assertEqual(result1, result3)
        self.assertEqual(result1, os.path.join(self.cwd, "testDir"))

    def testCdExceptions(self):
        with self.assertRaises(InvalidArgumentError):
            self.doOutputTest(
                ["testDir", "smh"], self.cwd, getEnv=True
            )  # Too many arguments
        with self.assertRaises(InvalidArgumentError):
            self.doOutputTest([], self.cwd, getEnv=True)  # No argument
        with self.assertRaises(InvalidFileOrDir):
            self.doOutputTest(["smh"], self.cwd, getEnv=True)  # Not existing directory
        self.assertTrue(
            "InvalidArgumentError"
            in self.doOutputTest(arg=["testDir", "smh"], env=self.cwd, unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.doOutputTest(arg=[], env=self.cwd, unsafeApp=True)
        )
        self.assertTrue(
            "InvalidFileOrDir"
            in self.doOutputTest(arg=["smh"], env=self.cwd, unsafeApp=True)
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
