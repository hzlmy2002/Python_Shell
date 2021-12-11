import sys

sys.path.insert(0, "../src")
from apps import *
import unittest, os, sys, io
from appTests import appTests
from shell import eval


class testStdin(unittest.TestCase):
    def setUp(self) -> None:
        with open("test1.txt", "w") as f:
            f.write("AAA\nBBB\nAAA")

    def tearDown(self) -> None:
        os.remove("test1.txt")

    def getStdOut(self, cmdLine):
        old = sys.stdout
        new = io.StringIO()
        sys.stdout = new
        eval(cmdLine)
        output = new.getvalue()
        sys.stdout = old
        return output

    def assertOutput(self, cmd, result):
        output = self.getStdOut(cmd).strip()
        self.assertEqual(result, output)

    def testCatStdin(self):
        cmd = "echo AAA | cat"
        self.assertOutput(cmd, "AAA")

    def testCutStdin(self):
        cmd = "cat test1.txt | cut -b 1"
        self.assertOutput(cmd, "A\nB\nA")

    def testGrepStdin(self):
        cmd = "cat test1.txt | grep ..."
        self.assertOutput(cmd, "AAA\nBBB\nAAA")

    def testHeadStdin(self):
        pass

    def testSortStdin(self):
        pass

    def testTailStdin(self):
        pass

    def testUniqStdin(self):
        pass


if __name__ == "__main__":
    unittest.main()
