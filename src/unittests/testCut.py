import sys

sys.path.insert(0, "..")
from apps import tools
from apps import *
from apps.Stream import *
import unittest, os


class testApps(unittest.TestCase):
    def setUp(self) -> None:
        with open("testA.txt", "w") as file:
            file.write(
                "Hello World, this is Cut test\nMy name is something\nNice to meet\nyou all"
            )

    def tearDown(self) -> None:
        os.remove("testA.txt")

    def assertHelper(self, result1, result2, stringPattern):
        self.assertEqual(result1.params["main"], result2.params["main"])
        self.assertEqual(result1.params["main"][0], stringPattern)

    def testCutFile(self):
        stream = Stream(
            streamType.input, "cut", {"b": ["1", "2"], "main": ["testA.txt"]}, {}
        )
        stream2 = Stream(
            streamType.input,
            "cut",
            {"b": ["-2", "5-"], "main": ["testA.txt"]},
            {},
        )
        stream3 = Stream(
            streamType.input,
            "cut",
            {"b": ["3-5"], "main": ["testA.txt"]},
            {},
        )
        stream4 = Stream(
            streamType.input,
            "cut",
            {"b": ["4", "3-5", "-6"], "main": ["testA.txt"]},
            {},
        )  # Testing combining ranges
        stream5 = Stream(
            streamType.input,
            "cut",
            {"b": ["6-", "3-5"], "main": ["testA.txt"]},
            {},
        )  # Testing unordered ranges
        app = Cut()
        appUnsafe = CutUnsafe()
        result1 = app.exec(stream)
        result2 = appUnsafe.exec(stream)
        result3 = app.exec(stream2)
        result4 = appUnsafe.exec(stream2)
        result5 = app.exec(stream3)
        result6 = appUnsafe.exec(stream3)
        result7 = app.exec(stream4)
        result8 = appUnsafe.exec(stream4)
        result9 = app.exec(stream5)
        result10 = appUnsafe.exec(stream5)
        self.assertHelper(result1, result2, "He\nMy\nNi\nyo\n")
        self.assertHelper(
            result3,
            result4,
            "Heo World, this is Cut test\nMyame is something\nNi to meet\nyoall\n",
        )
        self.assertHelper(result5, result6, "llo\n na\nce \nu a\n")
        self.assertHelper(result7, result8, "Hello \nMy nam\nNice t\nyou al\n")
        self.assertHelper(
            result9,
            result10,
            "llo World, this is Cut test\n name is something\nce to meet\nu all\n",
        )

    def testCutStdin(self):
        stream = Stream(
            streamType.input,
            "cut",
            {"main": [tools.str2stdin("Hello World!\n")], "b": ["1"]},
            {},
        )
        app = Cut()
        appUnsafe = CutUnsafe()
        result1 = app.exec(stream)
        result2 = appUnsafe.exec(stream)
        self.assertEqual(result1.params["main"], result2.params["main"])
        self.assertEqual(result1.params["main"][0], "Hello World!\n")

    def testCutExceptions(self):
        msg = stdExceptionMessage()
        stream1 = Stream(
            streamType.input, "cut", {"main": ["testA.txt"]}, {}
        )  # No option b specified (wrong param num)
        stream2 = Stream(
            streamType.input, "cut", {"b": ["1"], "main": []}, {}
        )  # No File specified (wrong main arg)
        stream3 = Stream(
            streamType.input,
            "cut",
            {"b": [], "main": ["testA.txt"]},
            {},
        )  # No tags specified
        stream4 = Stream(
            streamType.input, "cut", {"b": ["1"], "main": ["smh"]}, {}
        )  # Invalid File specified
        stream5 = None
        stream6 = Stream(
            streamType.input,
            "cut",
            {"b": ["1"], "pattern2": ["vvv"], "main": ["testA.txt"]},
            {},
        )  # Too many parameters
        stream7 = Stream(
            streamType.input, "cut", {"b": ["4-1"], "main": ["testA.txt"]}, {}
        )  # Decreasing range
        stream8 = Stream(
            streamType.input, "cut", {"b": ["n-n"], "main": ["testA.txt"]}, {}
        )  # Invalid tags specified
        stream9 = Stream(
            streamType.input,
            "cut",
            {"b": ["n-n"], "main": ["testA.txt", "testB.txt"]},
            {},
        )  # To many main args specified
        app = Cut()
        appUnsafe = CutUnsafe()
        with self.assertRaises(Exception):
            app.exec(stream1)
        with self.assertRaises(Exception):
            app.exec(stream2)
        with self.assertRaises(Exception):
            app.exec(stream3)
        with self.assertRaises(Exception):
            app.exec(stream4)
        with self.assertRaises(Exception):
            app.exec(stream5)
        with self.assertRaises(Exception):
            app.exec(stream6)
        with self.assertRaises(Exception):
            app.exec(stream7)
        with self.assertRaises(Exception):
            app.exec(stream8)
        with self.assertRaises(Exception):
            app.exec(stream9)
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum)
            in appUnsafe.exec(stream1).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum)
            in appUnsafe.exec(stream2).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.tagNum)
            in appUnsafe.exec(stream3).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.file)
            in appUnsafe.exec(stream4).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none)
            in appUnsafe.exec(stream5).params["main"][0]
        )

        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum)
            in appUnsafe.exec(stream6).params["main"][0]
        )

        self.assertTrue(
            msg.exceptionMsg(exceptionType.decRange)
            in appUnsafe.exec(stream7).params["main"][0]
        )

        self.assertTrue(
            msg.exceptionMsg(exceptionType.tagType)
            in appUnsafe.exec(stream8).params["main"][0]
        )

        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum)
            in appUnsafe.exec(stream9).params["main"][0]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
