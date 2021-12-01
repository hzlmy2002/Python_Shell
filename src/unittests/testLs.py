import sys

sys.path.insert(0, "..")

from apps import *
import unittest, os
from apps.Exceptions import InvalidArgumentError, InvalidFileOrDir
from appTests import appTests
import shutil


class testLs(unittest.TestCase):
    def setUp(self) -> None:
        self.cwd = os.getcwd()
        parent = "testDir/"
        os.makedirs(parent + "test1")
        os.makedirs(parent + "test2")
        os.makedirs(parent + ".test3")
        os.mkdir("testDir2")
        self.tester = appTests(ls)

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        shutil.rmtree("testDir")
        shutil.rmtree("testDir2")

    def testLsListDir(self):
        # lsUnsafe = LsUnsafe()
        result1 = self.tester.doOuputTest(["testDir"], {})
        # result2 = lsUnsafe.exec(stream1)
        os.chdir("testDir")
        result3 = self.tester.doOuputTest([], {})
        # result4 = lsUnsafe.exec(stream2)
        # self.assertEqual(result1.params["main"][0], result2.params["main"][0])
        # self.assertEqual(result3.params["main"][0], result4.params["main"][0])
        self.assertEqual(result1, result3)
        self.assertEqual(result1, "test1\ntest2\n")

    def testLsExceptions(self):
        # lsUnsafe = LsUnsafe()
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["testDir", "testDir2"])  # Too many arguments
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest(["smh"])  # Not existing directory
        """self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum)
            in lsUnsafe.exec(stream1).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum)
            in lsUnsafe.exec(stream2).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.dir)
            in lsUnsafe.exec(stream3).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none)
            in lsUnsafe.exec(stream4).params["main"][0]
        )"""


if __name__ == "__main__":
    unittest.main(verbosity=2)
