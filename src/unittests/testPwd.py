import sys

sys.path.insert(0, "..")

from apps import *
import unittest, os
from appTests import appTests
from apps.Exceptions import InvalidArgumentError


class testPwd(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir("testDir")
        self.cwd = os.getcwd()
        self.tester = appTests(pwd)

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        os.rmdir("testDir")

    def testPwdChangeDir(self):
        # appUnsafe = PwdUnsafe()
        result1 = self.tester.doOuputTest(env={"workingDir": self.cwd})
        # result2 = appUnsafe.exec(stream)
        # os.chdir("testDir")
        # result3 = app.exec(stream)
        # result4 = appUnsafe.exec(stream)
        # self.assertEqual(result1.env, result2.env)
        self.assertEqual(result1, self.cwd + "\n")
        # self.assertEqual(result3.env, result4.env)
        """self.assertEqual(
            result3.params["main"][0], self.cwd + os.sep + "testDir" + "\n"
        )"""
        os.chdir(self.cwd)

    def testPwdExceptions(self):
        # appUnsafe = PwdUnsafe()
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["some args"])
        """self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum)
            in appUnsafe.exec(stream1).params["main"][0]
        )"""


if __name__ == "__main__":
    unittest.main(verbosity=2)
