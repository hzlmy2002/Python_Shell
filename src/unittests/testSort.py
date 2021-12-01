import sys

sys.path.insert(0, "..")
from apps import tools
from apps import *
from apps.Stream import *
import unittest, os


class testSort(unittest.TestCase):
    def setUp(self) -> None:
        with open("testA.txt", "w") as file:
            file.write(
                "Two roads diverged in a yello wood,\nAnd sorry I could not travel both\nAnd be one traveler,long I stood\nAnd looked down one as far as I could\nTo where it bent in the undergrowth"
            )

    def tearDown(self) -> None:
        os.remove("testA.txt")

    def matchHelper(self, result1, result2, stringPattern):
        self.assertEqual(result1.params["main"], result2.params["main"])
        self.assertEqual(result1.params["main"][0], stringPattern)

    def testSortFile(self):
        stream = Stream(streamType.input, "sort", {"main": ["testA.txt"]}, {})
        stream2 = Stream(streamType.input, "sort", {"r": [], "main": ["testA.txt"]}, {})
        app = Sort()
        appUnsafe = SortUnsafe()
        result1 = app.exec(stream)
        result2 = appUnsafe.exec(stream)
        result3 = app.exec(stream2)
        result4 = appUnsafe.exec(stream2)
        answer = [
            "And be one traveler,long I stood\n",
            "And looked down one as far as I could\n",
            "And sorry I could not travel both\n",
            "To where it bent in the undergrowth\n",
            "Two roads diverged in a yello wood,\n",
        ]
        self.matchHelper(
            result1,
            result2,
            "".join(answer),
        )
        self.matchHelper(result3, result4, "".join(answer[::-1]))

    def testSortStdin(self):
        stream = Stream(
            streamType.input,
            "sort",
            {"main": [tools.str2stdin("Hello World!\n")]},
            {},
        )
        app = Sort()
        appUnsafe = SortUnsafe()
        result1 = app.exec(stream)
        result2 = appUnsafe.exec(stream)
        self.assertEqual(result1.params["main"], result2.params["main"])
        self.assertEqual(result1.params["main"][0], "Hello World!\n")

    def testSortExceptions(self):
        msg = stdExceptionMessage()
        stream1 = Stream(
            streamType.input, "sort", {"main": ["testA.txt"], "a": [], "b": []}, {}
        )  # Too many parameters
        stream2 = Stream(streamType.input, "sort", {"main": []}, {})  # Empty main arg
        stream3 = Stream(
            streamType.input,
            "sort",
            {"r": ["BBB"], "main": ["testA.txt"]},
            {},
        )  # r tag contains a value
        stream4 = Stream(
            streamType.input, "sort", {"main": ["smh"]}, {}
        )  # Invalid File specified
        stream5 = None
        stream6 = Stream(
            streamType.input, "sort", {"main": ["testA.txt"], "a": []}, {}
        )  # Invalid option tag
        app = Sort()
        appUnsafe = SortUnsafe()
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
            msg.exceptionMsg(exceptionType.paramType)
            in appUnsafe.exec(stream6).params["main"][0]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
