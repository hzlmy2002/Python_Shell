import sys

sys.path.insert(0, "../src")
import os
import unittest
from withStdOut import withStdOut
import shutil


class testGlob(withStdOut):
    def setUp(self) -> None:
        os.mkdir("testFolder")
        os.chdir("testFolder")
        self.cwd = os.getcwd()
        with open("test.txt", "w"):
            pass
        with open("test2.txt", "w"):
            pass
        with open("pic.jpg", "w"):
            pass

    def tearDown(self) -> None:
        os.chdir("..")
        shutil.rmtree("testFolder")

    def testGlobTxt(self):
        self.assertOutput(
            "echo *.txt", "test2.txt test.txt", self.cwd, ignoreOrder=True
        )
        self.assertOutput("echo *.png", "no glob", self.cwd)


if __name__ == "__main__":
    unittest.main()
