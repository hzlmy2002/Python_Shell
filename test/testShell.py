import sys

sys.path.insert(0, "../src")
from apps import *
import unittest, os
from Tools import getStdOut

from shell import eval
from collections import deque


class TestShell(unittest.TestCase):
    def test_shell(self):
        pass


if __name__ == "__main__":
    unittest.main()
