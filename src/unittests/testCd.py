import sys

sys.path.insert(0, "..")

from apps import *
from apps.Stream import *
import unittest, os


class testApps(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir("testDir")
        self.cwd = os.getcwd()

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        os.rmdir("testDir")

    def testCdChangeDir(self):
        stream1 = Stream(
            streamType.input, "cd", {"main": ["testDir"]}, {"working_dir": self.cwd}
        )
        stream2 = Stream(
            streamType.input, "cd", {"main": [".."]}, {"working_dir": self.cwd}
        )
        cd = Cd()
        cdUnsafe = CdUnsafe()
        os.chdir(self.cwd)
        result1 = cd.exec(stream1)
        result2 = cd.exec(stream2)
        os.chdir(self.cwd)
        result3 = cdUnsafe.exec(stream1)
        result4 = cdUnsafe.exec(stream2)
        self.assertEqual(result1.env, result3.env)
        self.assertEqual(result1.env["working_dir"], self.cwd + os.sep + "testDir")
        self.assertEqual(result2.env, result4.env)
        self.assertEqual(result2.env["working_dir"], self.cwd)

    def testCdExceptions(self):
        msg = stdExceptionMessage()
        stream1 = Stream(streamType.input, "cat", {"main": ["testDir", "smh"]}, {})
        stream2 = Stream(streamType.input, "cat", {"a": [""], "main": ["testDir"]}, {})
        stream3 = Stream(streamType.input, "cat", {"main": ["smh"]}, {})
        stream4 = None
        cd = Cat()
        cdUnsafe = CdUnsafe()
        with self.assertRaises(Exception):
            cd.exec(stream1)
        with self.assertRaises(Exception):
            cd.exec(stream2)
        with self.assertRaises(Exception):
            cd.exec(stream3)
        with self.assertRaises(Exception):
            cd.exec(stream4)
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum)
            in cdUnsafe.exec(stream1).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum)
            in cdUnsafe.exec(stream2).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.dir)
            in cdUnsafe.exec(stream3).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none)
            in cdUnsafe.exec(stream4).params["main"][0]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
