import os
import unittest
from appTests import appTests
from apps.Exceptions import (
    InvalidArgumentError,
    InvalidParamTagError,
    InvalidFileOrDir,
)
from apps.Uniq import uniq
import sys

sys.path.insert(0, "../src")


class testUniq(unittest.TestCase):
    def setUp(self) -> None:
        with open("testA.txt", "w") as file:
            file.write(
                "Hello Hello\nHELLO HELLO\nHello World\n" +
                "HelloHello\nHelloHello\nHelloHello\nWorld\nWorld\nWorld"
            )
        with open("testB.txt", "w") as file:
            file.write(
                "Hello Hello\nHELLO HELLO\nHello World\nHelloHello\n" +
                "HelloHello\nHelloHello\nWorld\nWorld\nWorld\n"
            )
        self.tester = appTests(uniq)

    def tearDown(self) -> None:
        os.remove("testA.txt")
        os.remove("testB.txt")

    def matchHelper(self, result1, result2, stringPattern):
        self.assertEqual(result1, result2)
        self.assertEqual(result1, stringPattern)

    def testUniqFile(self):
        result1 = self.tester.doOuputTest(["testA.txt"])
        result2 = self.tester.doOuputTest(["testA.txt"], unsafeApp=True)
        result3 = self.tester.doOuputTest(["-i", "testA.txt"])
        result4 = self.tester.doOuputTest(["-i", "testA.txt"], unsafeApp=True)
        result5 = self.tester.doOuputTest(["testB.txt"])
        result6 = self.tester.doOuputTest(["testB.txt"], unsafeApp=True)
        result7 = self.tester.doOuputTest(["-i", "testB.txt"])
        result8 = self.tester.doOuputTest(["-i", "testB.txt"], unsafeApp=True)
        self.matchHelper(
            result1,
            result2,
            "Hello Hello\nHELLO HELLO\nHello World\nHelloHello\nWorld\nWorld",
        )
        self.matchHelper(
            result3,
            result4,
            "Hello Hello\nHello World\nHelloHello\nWorld\nWorld",
        )
        self.matchHelper(
            result5,
            result6,
            "Hello Hello\nHELLO HELLO\nHello World\nHelloHello\nWorld\n",
        )
        self.matchHelper(
            result7,
            result8,
            "Hello Hello\nHello World\nHelloHello\nWorld\n",
        )

    def testUniqExceptions(self):
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(
                ["testB.txt", "testA.txt"])  # Too many arguments
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([])  # Empty argument
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(
                ["-i", "123", "testA.txt"])  # Too many arguments
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest(["-i", "smh"])  # Not existing file
        with self.assertRaises(InvalidParamTagError):
            self.tester.doOuputTest(["-a", "testA.txt"])  # Invalid flag A
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([""])  # Empty
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([])  # Empty
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["testB.txt", "testA.txt"],
                                       unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError" in self.tester.doOuputTest(
                [], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["-i", "123", "testA.txt"],
                                       unsafeApp=True)
        )
        self.assertTrue(
            "InvalidFileOrDir" in self.tester.doOuputTest(
                ["-i", "smh"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidParamTagError"
            in self.tester.doOuputTest(["-a", "testA.txt"], unsafeApp=True)
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
