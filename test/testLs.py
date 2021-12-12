import sys

sys.path.insert(0, "../src")
import os
import unittest
import shutil
from appTests import appTests
from apps.Exceptions import InvalidArgumentError, InvalidFileOrDir
from apps.Ls import ls

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
        result1 = self.tester.doOuputTest(["testDir"])
        result2 = self.tester.doOuputTest(["testDir"], unsafeApp=True)
        os.chdir("testDir")
        result3 = self.tester.doOuputTest()
        result4 = self.tester.doOuputTest(unsafeApp=True)
        self.assertEqual(result1, result2)
        self.assertEqual(result3, result4)
        self.assertEqual(result1, result3)
        self.assertEqual(result1, "test1\ntest2\n")

    def testLsExceptions(self):
        # lsUnsafe = LsUnsafe()
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(
                ["testDir", "testDir2"])  # Too many arguments
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest(["smh"])  # Not existing directory
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["testDir", "testDir2"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidFileOrDir" in self.tester.doOuputTest(
                ["smh"], unsafeApp=True)
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
