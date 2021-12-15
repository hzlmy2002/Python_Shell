import sys
import unittest

sys.path.insert(0, "../src")
import os
from withStdOut import withStdOut
from shell import Shell


class testSubstitution(withStdOut):
    def testSubs(self):
        self.assertOutput("echo `echo AAA`", "AAA")
        self.assertOutput("echo A`echo A`A", "AAA")
        self.assertOutput("echo `echo AAA  BBB`", "AAA BBB")
        self.assertOutput("`echo echo` AAA", "AAA")


if __name__ == "__main__":
    unittest.main()
