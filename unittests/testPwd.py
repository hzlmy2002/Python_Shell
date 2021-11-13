import sys

sys.path.insert(1, "../src")

from apps import *
from Stream import *
import unittest, os
from standardStreamExceptions import *


class testApps(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir("testDir")
        self.cwd = os.getcwd()

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        os.rmdir("testDir")

    def testPwdChangeDir(self):
        stream = Stream(streamType.input, "pwd", [], [], {})
        app = Pwd()
        appUnsafe = PwdUnsafe()
        result1 = app.exec(stream)
        result2 = appUnsafe.exec(stream)
        os.chdir("testDir")
        result3 = app.exec(stream)
        result4 = appUnsafe.exec(stream)
        self.assertEqual(result1.env, result2.env)
        self.assertEqual(result1.getArgs()[0], self.cwd + "\n")
        self.assertEqual(result3.env, result4.env)
        self.assertEqual(result3.getArgs()[0], self.cwd + "/testDir" + "\n")
        os.chdir(self.cwd)

    def testPwdExceptions(self):
        msg = stdExceptionMessage()
        stream1 = Stream(streamType.input, "pwd", [], ["smh"], {})  # Contains argument
        stream2 = Stream(
            streamType.input, "pwd", [], ["smh", "smh"], {}
        )  # Contains arguments
        stream3 = Stream(streamType.input, "pwd", ["smh"], [], {})  # Contains parameter
        stream4 = Stream(
            streamType.input, "pwd", ["smh", "smh"], [], {}
        )  # Contains parameters
        stream5 = None
        app = Pwd()
        appUnsafe = PwdUnsafe()
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
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum) in appUnsafe.exec(stream1).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum) in appUnsafe.exec(stream2).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum) in appUnsafe.exec(stream3).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum) in appUnsafe.exec(stream4).args[0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none) in appUnsafe.exec(stream5).args[0]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
