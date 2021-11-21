import sys
from unittest.main import main

sys.path.insert(0, "..")
from apps import *
from apps.Stream import *
from apps import tools
import unittest, os


class testApps(unittest.TestCase):
    def setUp(self) -> None:
        with open(".testCatA.txt", "w") as file:
            file.write("testCatA\n")
        with open(".testCatB.txt", "w") as file:
            file.write("testCatB")

    def tearDown(self) -> None:
        os.remove(".testCatA.txt")
        os.remove(".testCatB.txt")

    def testCatFile(self):
        stream = Stream(
            streamType.input, "cat", {"main":[".testCatA.txt", ".testCatB.txt"]}, {}
        )
        cat1 = Cat()
        cat2 = CatUnsafe()
        result1 = cat1.exec(stream)
        result2 = cat2.exec(stream)
        self.assertEqual(result1.params["main"], result2.params["main"])
        self.assertEqual(result1.params["main"][0], "testCatA\ntestCatB")

    def testCatStdin(self):
        stream = Stream(
            streamType.input, "cat", {"main":[tools.str2stdin("Hello World!\n")]}, {}
        )
        cat1 = Cat()
        cat2 = CatUnsafe()
        result1 = cat1.exec(stream)
        result2 = cat2.exec(stream)
        self.assertEqual(result1.params["main"], result2.params["main"])
        self.assertEqual(result1.params["main"][0], "Hello World!\n")


    def testCatExceptions(self):
        msg = stdExceptionMessage()
        stream1 = Stream(streamType.input, "cat", {"main":["^^^"]}, {})
        stream2 = Stream(streamType.input, "cat", {"a": [""],"main":[]}, {})
        stream3 = Stream(streamType.input, "cat", {"main":[tools.str2stdin("aaaa"), ""]}, {})
        stream4 = None
        stream5 = Stream(streamType.input, "cat", {"a": [],"main":[]}, {})
        cat1 = Cat()
        cat2 = CatUnsafe()
        with self.assertRaises(Exception):
            cat1.exec(stream1)
        with self.assertRaises(Exception):
            cat1.exec(stream2)
        with self.assertRaises(Exception):
            cat1.exec(stream3)
        with self.assertRaises(Exception):
            cat1.exec(stream4)
        with self.assertRaises(Exception):
            cat1.exec(stream5)
        self.assertTrue(
            msg.exceptionMsg(exceptionType.file) in cat2.exec(stream1).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum) in cat2.exec(stream2).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.stdin) in cat2.exec(stream3).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none) in cat2.exec(stream4).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum) in cat2.exec(stream5).params["main"][0]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
