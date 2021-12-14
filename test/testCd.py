import sys

sys.path.insert(0, "../src")
import os
import unittest
from appTests import appTests
from apps.Exceptions import InvalidArgumentError, InvalidFileOrDir
from apps.Cd import cd


class testCd(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir("testDir")
        self.cwd = os.getcwd()
        self.tester = appTests(cd)

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        os.rmdir("testDir")

    def testCdChangeDir(self):
        result1 = self.tester.changeEnvTest(["testDir"], env=self.cwd)
        os.chdir(self.cwd)
        result3 = self.tester.changeEnvTest(["testDir"], env=self.cwd, unsafeApp=True)
        self.assertEqual(result1, result3)
        self.assertEqual(result1, os.path.join(self.cwd, "testDir"))

    def testCdExceptions(self):
        with self.assertRaises(InvalidArgumentError):
            self.tester.changeEnvTest(
                ["testDir", "smh"], self.cwd
            )  # Too many arguments
        with self.assertRaises(InvalidArgumentError):
            self.tester.changeEnvTest([], self.cwd)  # No argument
        with self.assertRaises(InvalidFileOrDir):
            self.tester.changeEnvTest(["smh"], self.cwd)  # Not existing directory
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["testDir", "smh"], env=self.cwd, unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest([], env=self.cwd, unsafeApp=True)
        )
        self.assertTrue(
            "InvalidFileOrDir"
            in self.tester.doOuputTest(["smh"], env=self.cwd, unsafeApp=True)
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
