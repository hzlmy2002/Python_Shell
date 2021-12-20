import sys
import os

sys.path.insert(0, "../src")
import unittest
from shell import Shell

class TestShell(unittest.TestCase):
    def testShell(self):
        sh=Shell(os.getcwd())
        sh.eval("   ",sys.stdout)
        self.assertEqual(sh.getWorkingDir(),os.getcwd())

if __name__ == "__main__":
    unittest.main()
