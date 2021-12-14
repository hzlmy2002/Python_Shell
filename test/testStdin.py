import sys

sys.path.insert(0, "../src")
import os
import unittest
from Tools import getStdOut


class testStdin(unittest.TestCase):
    def setUp(self) -> None:
        with open("test1.txt", "w") as f:
            f.write("AAA\nBBB\nAAA\n")

    def tearDown(self) -> None:
        os.remove("test1.txt")

    def assertOutput(self, cmd, result):
        output = getStdOut(cmd).strip()
        self.assertEqual(result, output)

    # def testCatStdin(self):
    #     cmd = "echo AAA | cat"
    #     self.assertOutput(cmd, "AAA")

    def testCutStdin(self):
        cmd = "cat test1.txt | cut -b 1"
        self.assertOutput(cmd, "A\nB\nA")

    def testGrepStdin(self):
        cmd = "cat test1.txt | grep ..."
        self.assertOutput(cmd, "AAA\nBBB\nAAA")

    def testHeadStdin(self):
        cmd = "cat test1.txt | head -n 2"
        self.assertOutput(cmd, "AAA\nBBB")

    def testSortStdin(self):
        cmd = "cat test1.txt | sort"
        self.assertOutput(cmd, "AAA\nAAA\nBBB")

    def testTailStdin(self):
        cmd = "cat test1.txt | tail -n 2"
        self.assertOutput(cmd, "BBB\nAAA")

    def testUniqStdin(self):
        cmd = "cat test1.txt | uniq"
        self.assertOutput(cmd, "AAA\nBBB\nAAA")

    def testLongPipe(self):
        cmd = "cat test1.txt | uniq | head -n 2"
        self.assertOutput(cmd, "AAA\nBBB")


if __name__ == "__main__":
    unittest.main()
