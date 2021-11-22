import sys

sys.path.insert(0, "..")
from apps import *
from apps.Stream import *
import unittest, os
import shutil


class testApps(unittest.TestCase):
    def setUp(self) -> None:
        os.makedirs("root/testDir/test1")
        os.mkdir("root/testDir2/")
        f1 = open("root/test1.txt", "a")
        f1.close()
        f2 = open("root/testDir/test2.txt", "a")
        f2.close()
        f3 = open("root/testDir/Alttest1.txt", "a")
        f3.close()
        f4 = open("root/testDir/test1/test3.txt", "a")
        f4.close()
        f5 = open("root/testDir2/test4.txt", "a")
        f5.close()

    def tearDown(self) -> None:
        shutil.rmtree("root")

    def testFindListFile(self):
        stream1 = Stream(
            streamType.input,
            "find",
            {"main": ["root"], "pattern": ["test*.txt"]},
            {},
        )
        stream2 = Stream(
            streamType.input, "find", {"main": ["root"], "pattern": ["Alt*.txt"]}, {}
        )
        app = Find()
        appUnsafe = FindUnsafe()
        result1 = app.exec(stream1)
        result2 = appUnsafe.exec(stream1)
        result3 = app.exec(stream2)
        result4 = appUnsafe.exec(stream2)
        self.assertEqual(result1.params["main"][0], result2.params["main"][0])
        self.assertEqual(result3.params["main"][0], result4.params["main"][0])
        self.assertEqual(
            result1.params["main"][0],
            "root/test1.txt\nroot/testDir/test2.txt\nroot/testDir/test1/test3.txt\nroot/testDir2/test4.txt\n",
        )
        self.assertEqual(result3.params["main"][0], "root/testDir/Alttest1.txt\n")

    def testFindExceptions(self):
        msg = stdExceptionMessage()
        stream1 = Stream(
            streamType.input,
            "find",
            {"main": ["root", "testDir2"], "pattern": ["somepattern"]},
            {},
        )  # Two main args specified
        stream2 = Stream(
            streamType.input, "find", {"smh": ["a"], "main": ["root"]}, {}
        )  # Invalid tag type
        stream3 = Stream(
            streamType.input, "find", {"main": ["smh"], "pattern": ["somepattern"]}, {}
        )  # Non existing dir specified
        stream4 = None
        stream5 = Stream(
            streamType.input,
            "find",
            {"main": ["root"], "pattern": ["somepattern", "somemorepattern"]},
            {},
        )  # Too many tags specified

        stream6 = Stream(
            streamType.input,
            "find",
            {"main": ["root"], "pattern": ["somepattern"], "pattern2": ["somepattern"]},
            {},
        )  # Too many tags specified
        app = Find()
        appUnsafe = FindUnsafe()
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
            msg.exceptionMsg(exceptionType.argNum)
            in appUnsafe.exec(stream1).params["main"][0]
        )

        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramType)
            in appUnsafe.exec(stream2).params["main"][0]
        )

        self.assertTrue(
            msg.exceptionMsg(exceptionType.dir)
            in appUnsafe.exec(stream3).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none)
            in appUnsafe.exec(stream4).params["main"][0]
        )

        self.assertTrue(
            msg.exceptionMsg(exceptionType.tagNum)
            in appUnsafe.exec(stream5).params["main"][0]
        )

        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum)
            in appUnsafe.exec(stream6).params["main"][0]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
