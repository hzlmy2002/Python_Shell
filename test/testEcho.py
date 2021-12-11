import sys

sys.path.insert(0, "..")
from apps import *
import unittest
from appTests import appTests


class testEcho(unittest.TestCase):
    def setUp(self) -> None:
        self.tester = appTests(echo)

    def testEchoOutput(self):
        result1 = self.tester.doOuputTest(["Hello"])
        result2 = self.tester.doOuputTest(["Hello"], unsafeApp=True)
        self.assertEqual(result1, "Hello\n")
        self.assertEqual(result1, result2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
