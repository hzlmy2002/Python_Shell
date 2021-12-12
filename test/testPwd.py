import os
import unittest
from apps.Exceptions import InvalidArgumentError
from appTests import appTests
from apps.Pwd import pwd
import sys

sys.path.insert(0, "../src")


class testPwd(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir("testDir")
        self.cwd = os.getcwd()
        self.tester = appTests(pwd)

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        os.rmdir("testDir")

    def testPwdChangeDir(self):
        result1 = self.tester.doOuputTest(env={"workingDir": self.cwd})
        result2 = self.tester.doOuputTest(
            env={"workingDir": self.cwd}, unsafeApp=True)
        self.assertEqual(result1, result2)
        self.assertEqual(result1, self.cwd + "\n")

    def testPwdExceptions(self):
        # appUnsafe = PwdUnsafe()
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["some args"])
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["some args"], unsafeApp=True)
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
