import sys

sys.path.insert(0, "..")

from apps import *
from apps.Stream import *
import unittest, os
from StreamForTest import StreamForTest
from apps.Exceptions import InvalidArgumentError, InvalidFileOrDir
from apps.decorators import unsafe
from appTests import appTests


class testCd(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir("testDir")
        self.cwd = os.getcwd()
        self.tester = appTests(cd)

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        os.rmdir("testDir")

    def testCdChangeDir(self):
        result1 = self.tester.changeEnvTest(["testDir"], {"workingDir": self.cwd})
        result2 = self.tester.changeEnvTest(
            [".."], {"workingDir": os.path.join(self.cwd, "testDir")}
        )
        result3 = self.tester.changeEnvTest(
            ["testDir"], {"workingDir": self.cwd}, unsafeApp=True
        )
        result4 = self.tester.changeEnvTest(
            [".."], {"workingDir": os.path.join(self.cwd, "testDir")}, unsafeApp=True
        )
        self.assertEqual(result1, result3)
        self.assertEqual(result1, os.path.join(self.cwd, "testDir"))
        self.assertEqual(result2, result4)
        self.assertEqual(result2, self.cwd)

    def testCdExceptions(self):
        with self.assertRaises(InvalidArgumentError):
            self.tester.changeEnvTest(
                ["testDir", "smh"], {"workingDir": self.cwd}
            )  # Too many arguments
        with self.assertRaises(InvalidArgumentError):
            self.tester.changeEnvTest([], {"workingDir": self.cwd})  # No argument
        with self.assertRaises(InvalidArgumentError):
            self.tester.changeEnvTest([""], {"workingDir": self.cwd})  # No argument
        with self.assertRaises(InvalidFileOrDir):
            self.tester.changeEnvTest(
                ["smh"], {"workingDir": self.cwd}
            )  # Not existing directory
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(
                ["testDir", "smh"], {"workingDir": self.cwd}, unsafeApp=True
            )
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest([], {"workingDir": self.cwd}, unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest([""], {"workingDir": self.cwd}, unsafeApp=True)
        )
        self.assertTrue(
            "InvalidFileOrDir"
            in self.tester.doOuputTest(
                ["smh"], {"workingDir": self.cwd}, unsafeApp=True
            )
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
