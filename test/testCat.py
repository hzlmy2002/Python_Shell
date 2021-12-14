import sys

sys.path.insert(0, "../src")
import os
import unittest
from apps.Exceptions import InvalidFileOrDir, MissingStdin
from appTests import appTests
from apps.Cat import cat


class testCat(unittest.TestCase):
    def setUp(self) -> None:
        with open(".testCatA.txt", "w") as file:
            file.write("TestLineA\nTestLineAA\n")
        with open(".testCatB.txt", "w") as file:
            file.write("testCatB")
        self.tester = appTests(cat)

    def tearDown(self) -> None:
        os.remove(".testCatA.txt")
        os.remove(".testCatB.txt")

    def testCatFile(self):
        result1 = self.tester.doOuputTest([".testCatA.txt", ".testCatB.txt"])
        result2 = self.tester.doOuputTest(
            [".testCatA.txt", ".testCatB.txt"], unsafeApp=True
        )
        self.assertEqual(result1, result2)
        self.assertEqual(result1, "TestLineA\nTestLineAA\ntestCatB\n")

    def testCatExceptions(self):
        # cat2 = CatUnsafe()
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest(["^^^"])  # Not existing file
        with self.assertRaises(MissingStdin):
            self.tester.doOuputTest([])  # No argument
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest([""])  # No argument
        self.assertTrue(
            "InvalidFileOrDir" in self.tester.doOuputTest(["^^^"], unsafeApp=True)
        )
        self.assertTrue(
            "InvalidFileOrDir" in self.tester.doOuputTest([""], unsafeApp=True)
        )
        self.assertTrue("MissingStdin" in self.tester.doOuputTest([], unsafeApp=True))


if __name__ == "__main__":
    unittest.main(verbosity=2)
