import sys

sys.path.insert(0, "../src")
import os
from withStdOut import withStdOut
from shell import Shell
import unittest


class testRedirection(withStdOut):
    def setUp(self) -> None:
        with open("test.txt", "w") as f:
            f.write("AAA\nBBB\nCCC")

    def tearDown(self) -> None:
        os.remove("test.txt")

    def testInRedirection(self):
        self.assertOutput("cat < test.txt", "AAA\nBBB\nCCC")
        with self.assertRaises(FileNotFoundError):
            self.assertOutput("cat < noFile.txt", "")

    def testOutRedirection(self):
        sh = Shell("")
        sh.eval("echo foo > testOut.txt", None)
        with open("testOut.txt") as f:
            self.assertEqual(f.read().strip(), "foo")
        os.remove("testOut.txt")


if __name__ == "__main__":
    unittest.main()
