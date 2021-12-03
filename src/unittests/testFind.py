import sys

sys.path.insert(0, "..")

from apps import *
import unittest, os
from apps.Exceptions import (
    InvalidArgumentError,
    InvalidParamError,
    InvalidFileOrDir,
    InvalidParamTagError,
    MissingParamError,
)
from appTests import appTests
import shutil


class testFind(unittest.TestCase):
    def setUp(self) -> None:
        os.makedirs("root/testDir/test1")
        os.mkdir("root/testDir2/")
        f1 = open("root/test1.txt", "a")
        f1.close()
        f2 = open("root/testDir/test2.txt", "a")
        f2.close()
        f3 = open("root/testDir/Alttest1.txt", "a")
        f3.close()
        f4 = open("root/testDir/test1/test3.txt", "a")
        f4.close()
        f5 = open("root/testDir2/test4.txt", "a")
        f5.close()
        self.tester = appTests(find)

    def tearDown(self) -> None:
        shutil.rmtree("root")

    def testFindListFile(self):
        result1 = self.tester.doOuputTest(["root", "-name", "test*.txt"])
        result2 = self.tester.doOuputTest(
            ["root", "-name", "test*.txt"], unsafeApp=True
        )
        result3 = self.tester.doOuputTest(["root", "-name", "Alt*.txt"])
        result4 = self.tester.doOuputTest(["root", "-name", "Alt*.txt"], unsafeApp=True)
        result5 = self.tester.doOuputTest(["-name", "test*.txt"])
        result6 = self.tester.doOuputTest(["-name", "test*.txt"], unsafeApp=True)
        self.assertEqual(result1, result2)
        self.assertEqual(result3, result4)
        self.assertEqual(result5, result6)
        self.assertEqual(
            result1,
            "root/test1.txt\nroot/testDir/test2.txt\nroot/testDir/test1/test3.txt\nroot/testDir2/test4.txt\n",
        )
        self.assertEqual(result3, "root/testDir/Alttest1.txt\n")
        self.assertEqual(
            result5,
            "./root/test1.txt\n./root/testDir/test2.txt\n./root/testDir/test1/test3.txt\n./root/testDir2/test4.txt\n",
        )

    def testFindExceptions(self):
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(
                ["root", "testDir2", "-name", "somepattern"]
            )  # Too many arguments
        with self.assertRaises(MissingParamError):
            self.tester.doOuputTest(
                ["root", "testDir2", "something", "somepattern"]
            )  # No -name tag
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest(
                ["smh", "-name", "somepattern"]
            )  # Not existing path smh
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(
                ["root", "-name", "somepattern", "somemorepattern"]
            )  # Too many patterns (too many arguments)
        with self.assertRaises(InvalidParamError):
            self.tester.doOuputTest(["root", "-name", "?est.txt"])  # Invalid Pattern
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(
                ["root", "testDir2", "-name", "somepattern"], unsafeApp=True
            )
        )

        self.assertTrue(
            "MissingParamError"
            in self.tester.doOuputTest(
                ["root", "testDir2", "something", "somepattern"], unsafeApp=True
            )
        )

        self.assertTrue(
            "InvalidFileOrDir"
            in self.tester.doOuputTest(["smh", "-name", "somepattern"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(
                ["root", "-name", "somepattern", "somemorepattern"], unsafeApp=True
            )
        )

        self.assertTrue(
            "InvalidParamError"
            in self.tester.doOuputTest(["root", "-name", "?est.txt"], unsafeApp=True)
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
