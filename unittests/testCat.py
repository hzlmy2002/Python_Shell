import sys

sys.path.insert(1, "../src")

from apps import *
from Stream import *
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
            streamType.input, "cat", [], [".testCatA.txt", ".testCatB.txt"], {}
        )
        cat1 = Cat()
        cat2 = CatUnsafe()
        result1 = cat1.exec(stream)
        result2 = cat2.exec(stream)
        self.assertEqual(result1.args[0], result2.args[0])
        self.assertEqual(result1.args[0], "testCatA\ntestCatB")

    def testCatStdin(self):
        stream = Stream(
            streamType.input, "cat", [], [tools.str2stdin("Hello World!\n")], {}
        )
        cat1 = Cat()
        cat2 = CatUnsafe()
        result1 = cat1.exec(stream)
        result2 = cat2.exec(stream)
        self.assertEqual(result1.args[0], result2.args[0])
        self.assertEqual(result1.args[0], "Hello World!\n")

    def testCatExceptions(self):
        stream1 = Stream(streamType.input, "cat", [], ["^^^"], {})
        stream2 = Stream(streamType.input, "cat", ["a"], [""], {})
        stream3 = Stream(streamType.input, "cat", [], [tools.str2stdin("aaaa"), ""], {})
        stream4 = None
        stream5 = Stream(streamType.input, "cat", ["a"], [], {})
        cat1 = Cat()
        cat2 = CatUnsafe()
        with self.assertRaises(FileNotFoundError):
            cat1.exec(stream1)
        with self.assertRaises(Exception):
            cat1.exec(stream2)
        with self.assertRaises(Exception):
            cat1.exec(stream3)
        with self.assertRaises(Exception):
            cat1.exec(stream4)
        with self.assertRaises(Exception):
            cat1.exec(stream5)
        self.assertTrue("FileNotFoundError" in cat2.exec(stream1).args[0])
        self.assertTrue(
            "Invalid number of command line parameters" in cat2.exec(stream2).args[0]
        )
        self.assertTrue("Ilegal stdin" in cat2.exec(stream3).args[0])
        self.assertTrue("No stream to process" in cat2.exec(stream4).args[0])
        self.assertTrue(
            "Invalid number of command line arguments" in cat2.exec(stream5).args[0]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
