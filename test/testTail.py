import os
import unittest
from appTests import appTests
from apps.Exceptions import (
    InvalidArgumentError,
    InvalidFileOrDir,
    InvalidParamTagError,
)
from apps.Tail import tail
import sys

sys.path.insert(0, "../src")


class testTail(unittest.TestCase):
    def setUp(self) -> None:
        with open("test.txt", "w") as file:
            file.write("l1\nl2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\nl12\n")
        self.tester = appTests(tail)

    def tearDown(self) -> None:
        os.remove("test.txt")

    def testTailFile(self):
        # tailUnsafe = TailUnsafe()
        result1 = self.tester.doOuputTest(["test.txt"])
        # result2 = tailUnsafe.exec(stream1)
        result3 = self.tester.doOuputTest(["-n", "11", "test.txt"])
        # result4 = tailUnsafe.exec(stream2)
        # self.assertEqual(result1, result2.params["main"][0])
        self.assertEqual(
            result1, "l3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\nl12\n")
        # self.assertEqual(result3.params["main"][0],result3.params["main"][0])
        self.assertEqual(
            result3, "l2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\nl12\n")

    def testTailExceptions(self):
        with self.assertRaises(InvalidParamTagError):
            # Invalid param tag -a
            self.tester.doOuputTest(["-a", "11", "test.txt"])
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(
                ["-n", "11", "smh", "test.txt"]
            )  # Way to many arguments
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest(
                ["-n", "11", "smh.txt"])  # Not existing file

        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["-n", "11"])  # No file specified

        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["-n", "11", ""])  # No file specified

        with self.assertRaises(InvalidArgumentError):
            # No param argument specified
            self.tester.doOuputTest(["-n", "test.txt"])
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([""])  # Empty
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([])  # Empty

        self.assertTrue(
            "InvalidParamTagError"
            in self.tester.doOuputTest(["-a", "11", "test.txt"],
                                       unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["-n", "11", "smh", "test.txt"],
                                       unsafeApp=True)
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
            "InvalidArgumentError" in self.tester.doOuputTest(
                [""], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError" in self.tester.doOuputTest(
                [], unsafeApp=True)
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
