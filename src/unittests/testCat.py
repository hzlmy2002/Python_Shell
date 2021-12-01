import sys
from unittest.main import main

sys.path.insert(0, "..")
from apps import *
import unittest, os
from appTests import appTests
from apps.Exceptions import InvalidFileOrDir


class testCat(unittest.TestCase):
    def setUp(self) -> None:
        with open(".testCatA.txt", "w") as file:
            file.write("TestLineA\nTestLineAA\n")
        with open(".testCatB.txt", "w") as file:
            file.write("testCatB")
        self.tester = appTests(cat)

    def tearDown(self) -> None:
        os.remove(".testCatA.txt")
        os.remove(".testCatB.txt")

    def testCatFile(self):
        # cat2 = CatUnsafe()
        result1 = self.tester.doOuputTest([".testCatA.txt", ".testCatB.txt"])
        # result2 = cat2.exec(stream)
        # self.assertEqual(result1.params["main"], result2.params["main"])
        self.assertEqual(result1, "TestLineA\nTestLineAA\ntestCatB")

    """def testCatStdin(self):
        stream = Stream(
            streamType.input, "cat", {"main": [tools.str2stdin("Hello World!\n")]}, {}
        )
        cat1 = Cat()
        cat2 = CatUnsafe()
        result1 = cat1.exec(stream)
        result2 = cat2.exec(stream)
        self.assertEqual(result1.params["main"], result2.params["main"])
        self.assertEqual(result1.params["main"][0], "Hello World!\n")"""

    def testCatExceptions(self):
        # cat2 = CatUnsafe()
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest(["^^^"])  # Not existing file
        """self.assertTrue(
            msg.exceptionMsg(exceptionType.file) in cat2.exec(stream1).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum)
            in cat2.exec(stream2).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.stdin)
            in cat2.exec(stream3).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none) in cat2.exec(stream4).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum)
            in cat2.exec(stream5).params["main"][0]
        )"""


if __name__ == "__main__":
    unittest.main(verbosity=2)
