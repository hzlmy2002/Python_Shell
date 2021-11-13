import sys

sys.path.insert(1, "../src")
from apps import *
from Stream import *
import unittest, os
import shutil
from standardStreamExceptions import *


class testApps(unittest.TestCase):
    def setUp(self) -> None:
        self.cwd = os.getcwd()
        parent = "testDir/"
        os.makedirs(parent + "test1")
        os.makedirs(parent + "test2")
        os.makedirs(parent + ".test3")
        os.mkdir("testDir2")

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        shutil.rmtree("testDir")
        shutil.rmtree("testDir2")

    def testLsListDir(self):
        stream1 = Stream(streamType.input, "ls", [], ["testDir"], {})
        stream2 = Stream(streamType.input, "ls", [], [], {})
        ls = Ls()
        lsUnsafe = LsUnsafe()
        result1 = ls.exec(stream1)
        result2 = lsUnsafe.exec(stream1)
        os.chdir("testDir")
        result3 = ls.exec(stream2)
        result4 = lsUnsafe.exec(stream2)
        self.assertEqual(result1.getArgs()[0], result2.getArgs()[0])
        self.assertEqual(result3.getArgs()[0], result4.getArgs()[0])
        self.assertEqual(result1.getArgs()[0], result3.getArgs()[0])
        self.assertEqual(result1.getArgs()[0], "test1\ntest2\n")

    def testCdExceptions(self):
        msg = stdExceptionMessage()
        stream1 = Stream(
            streamType.input, "ls", [], ["testDir", "testDir2"], {}
        )  # Two paths specified
        stream2 = Stream(
            streamType.input, "ls", ["a"], ["testDir"], {}
        )  # contains parameter
        stream3 = Stream(
            streamType.input, "ls", [], ["smh"], {}
        )  # Non existing dir specified
        stream4 = None
        ls = Ls()
        lsUnsafe = LsUnsafe()
        with self.assertRaises(Exception):
            ls.exec(stream1)
        with self.assertRaises(Exception):
            ls.exec(stream2)
        with self.assertRaises(Exception):
            ls.exec(stream3)
        with self.assertRaises(Exception):
            ls.exec(stream4)
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum) in lsUnsafe.exec(stream1).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum) in lsUnsafe.exec(stream2).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.dir) in lsUnsafe.exec(stream3).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none) in lsUnsafe.exec(stream4).args[0]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
