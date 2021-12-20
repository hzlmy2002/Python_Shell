import sys

sys.path.insert(0, "../src")
import os
import unittest
from withStdOut import withStdOut


class testStdin(withStdOut):
    def setUp(self) -> None:
        with open("test1.txt", "w") as f:
            f.write("AAA\nBBB\nAAA\n")

    def tearDown(self) -> None:
        os.remove("test1.txt")

    # def testCatStdin(self):
    #     cmd = "echo AAA | cat"
    #     self.assertOutput(cmd, "AAA")

    def testCutStdin(self):
        cmd = "cat test1.txt | cut -b 1"
        self.assertOutput(cmd, "A\nB\nA")
        cmd2 = "cut -b 1 < test1.txt"
        self.assertOutput(cmd2, "A\nB\nA")

    def testGrepStdin(self):
        cmd = "cat test1.txt | grep ..."
        self.assertOutput(cmd, "AAA\nBBB\nAAA")

    def testHeadStdin(self):
        cmd = "cat test1.txt | head -n 2"
        cmd2 = "head -n 2 < test1.txt"
        self.assertOutput(cmd, "AAA\nBBB")
        self.assertOutput(cmd2, "AAA\nBBB")

    def testSortStdin(self):
        cmd = "cat test1.txt | sort"
        cmd2 = "sort < test1.txt"
        self.assertOutput(cmd, "AAA\nAAA\nBBB")
        self.assertOutput(cmd2, "AAA\nAAA\nBBB")

    def testTailStdin(self):
        cmd = "cat test1.txt | tail -n 2"
        cmd2 = "tail -n 2 < test1.txt"
        self.assertOutput(cmd, "BBB\nAAA")
        self.assertOutput(cmd2, "BBB\nAAA")

    def testUniqStdin(self):
        cmd = "cat test1.txt | uniq"
        cmd2 = "uniq < test1.txt"
        self.assertOutput(cmd, "AAA\nBBB\nAAA")
        self.assertOutput(cmd2, "AAA\nBBB\nAAA")

    def testLongPipe(self):
        cmd = "cat test1.txt | uniq | head -n 2"
        self.assertOutput(cmd, "AAA\nBBB")


if __name__ == "__main__":
    unittest.main()
