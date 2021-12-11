import sys

sys.path.insert(0, "../src")

from apps import *
import unittest, os
from apps.Exceptions import InvalidArgumentError, InvalidParamTagError, InvalidFileOrDir
from appTests import appTests


class testHead(unittest.TestCase):
    def setUp(self) -> None:
        self.tester = appTests(head)
        with open("test.txt", "w") as file:
            file.write("l1\nl2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\n")

    def tearDown(self) -> None:
        os.remove("test.txt")

    def testHeadFile(self):
        result1 = self.tester.doOuputTest(["test.txt"])
        result2 = self.tester.doOuputTest(["test.txt"], unsafeApp=True)
        result3 = self.tester.doOuputTest(["-n", "11", "test.txt"])
        result4 = self.tester.doOuputTest(["-n", "11", "test.txt"], unsafeApp=True)
        self.assertEqual(result1, result2)
        self.assertEqual(result1, "l1\nl2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\n")
        self.assertEqual(result3, result4)
        self.assertEqual(result3, "l1\nl2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\n")

    def testHeadExceptions(self):
        with self.assertRaises(InvalidParamTagError):
            self.tester.doOuputTest(["-a", "11", "test.txt"])  # Invalid param tag -a
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(
                ["-n", "11", "smh", "test.txt"]
            )  # Way to many arguments
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest(["-n", "11", "smh.txt"])  # Not existing file

        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["-n", "11"])  # No file specified

        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["-n", "11", ""])  # No file specified

        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["-n", "test.txt"])  # No param argument specified
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([""])  # Empty
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([])  # Empty
        self.assertTrue(
            "InvalidParamTagError"
            in self.tester.doOuputTest(["-a", "11", "test.txt"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["-n", "11", "smh", "test.txt"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidFileOrDir"
            in self.tester.doOuputTest(["-n", "11", "smh.txt"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["-n", "11"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["-n", "11", ""], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["-n", "test.txt"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError" in self.tester.doOuputTest([""], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError" in self.tester.doOuputTest([], unsafeApp=True)
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
