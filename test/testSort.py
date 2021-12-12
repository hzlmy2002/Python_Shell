import os
import unittest
from appTests import appTests
from apps.Exceptions import (
    InvalidArgumentError,
    InvalidFileOrDir,
    InvalidParamTagError,
)
from apps.Sort import sort
import sys

sys.path.insert(0, "../src")


class testSort(unittest.TestCase):
    def setUp(self) -> None:
        with open("testA.txt", "w") as file:
            file.write(
                "Two roads diverged in a yello wood,\n" +
                "And sorry I could not travel both\n" +
                "And be one traveler,long I stood\n" +
                "And looked down one as far as I could\n" +
                "To where it bent in the undergrowth"
            )
        self.tester = appTests(sort)

    def tearDown(self) -> None:
        os.remove("testA.txt")

    def matchHelper(self, result1, result2, stringPattern):
        self.assertEqual(result1, result2)
        self.assertEqual(result1, stringPattern)

    def testSortFile(self):
        result1 = self.tester.doOuputTest(["testA.txt"])
        result2 = self.tester.doOuputTest(["testA.txt"], unsafeApp=True)
        result3 = self.tester.doOuputTest(["-r", "testA.txt"])
        result4 = self.tester.doOuputTest(["-r", "testA.txt"], unsafeApp=True)
        answer = [
            "And be one traveler,long I stood\n",
            "And looked down one as far as I could\n",
            "And sorry I could not travel both\n",
            "To where it bent in the undergrowth\n",
            "Two roads diverged in a yello wood,\n",
        ]

        # Add unsafe later
        self.matchHelper(
            result1,
            result2,
            "".join(answer),
        )
        self.matchHelper(result3, result4, "".join(answer[::-1]))

    def testSortExceptions(self):
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(
                ["testB.txt", "testA.txt"])  # Too many arguments
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([])  # Empty argument
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([""])  # Empty argument
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["-r", ""])  # Empty argument
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["-r"])  # Empty argument
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(
                ["-r", "123", "testA.txt"])  # Too many arguments
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest(["-r", "smh"])  # Not existing file
        with self.assertRaises(InvalidParamTagError):
            self.tester.doOuputTest(["-a", "testA.txt"])  # Invalid flag A
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([""])  # Empty
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([])  # Empty
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(
                ["testB.txt", "testA.txt"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError" in self.tester.doOuputTest(
                [], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError" in self.tester.doOuputTest(
                [""], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(["-r", ""], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError" in self.tester.doOuputTest(
                ["-r"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidArgumentError"
            in self.tester.doOuputTest(
                ["-r", "123", "testA.txt"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidFileOrDir" in self.tester.doOuputTest(
                ["-r", "smh"], unsafeApp=True)
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
