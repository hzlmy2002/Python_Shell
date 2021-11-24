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
                "Hello Hello\nHELLO HELLO\nHello World\nHelloHello\nHelloHello\nHelloHello\nWorld\nWorld\nWorld"
            )
        with open("testB.txt", "w") as file:
            file.write(
                "Hello Hello\nHELLO HELLO\nHello World\nHelloHello\nHelloHello\nHelloHello\nWorld\nWorld\nWorld\n"
            )

    def tearDown(self) -> None:
        os.remove("testA.txt")
        os.remove("testB.txt")

    def matchHelper(self, result1, result2, stringPattern):
        self.assertEqual(result1.params["main"], result2.params["main"])
        self.assertEqual(result1.params["main"][0], stringPattern)

    def testUniqFile(self):
        stream = Stream(streamType.input, "uniq", {"main": ["testA.txt"]}, {})
        stream2 = Stream(streamType.input, "uniq", {"i": [], "main": ["testA.txt"]}, {})
        stream3 = Stream(
            streamType.input,
            "uniq",
            {"main": ["testB.txt"]},
            {},
        )
        stream4 = Stream(streamType.input, "uniq", {"i": [], "main": ["testB.txt"]}, {})
        app = Uniq()
        appUnsafe = UniqUnsafe()
        result1 = app.exec(stream)
        result2 = appUnsafe.exec(stream)
        result3 = app.exec(stream2)
        result4 = appUnsafe.exec(stream2)
        result5 = app.exec(stream3)
        result6 = appUnsafe.exec(stream3)
        result7 = app.exec(stream4)
        result8 = appUnsafe.exec(stream4)
        self.matchHelper(
            result1,
            result2,
            "Hello Hello\nHELLO HELLO\nHello World\nHelloHello\nWorld\nWorld",
        )
        self.matchHelper(
            result3, result4, "Hello Hello\nHello World\nHelloHello\nWorld\nWorld"
        )
        self.matchHelper(
            result5,
            result6,
            "Hello Hello\nHELLO HELLO\nHello World\nHelloHello\nWorld\n",
        )
        self.matchHelper(
            result7, result8, "Hello Hello\nHello World\nHelloHello\nWorld\n"
        )

    def testUniqStdin(self):
        stream = Stream(
            streamType.input,
            "uniq",
            {"main": [tools.str2stdin("Hello World!\n")]},
            {},
        )
        app = Uniq()
        appUnsafe = UniqUnsafe()
        result1 = app.exec(stream)
        result2 = appUnsafe.exec(stream)
        self.assertEqual(result1.params["main"], result2.params["main"])
        self.assertEqual(result1.params["main"][0], "Hello World!\n")

    def testUniqExceptions(self):
        msg = stdExceptionMessage()
        stream1 = Stream(
            streamType.input, "uniq", {"main": ["testA.txt"], "a": [], "b": []}, {}
        )  # Too many parameters
        stream2 = Stream(streamType.input, "grep", {"main": []}, {})  # Empty main arg
        stream3 = Stream(
            streamType.input,
            "grep",
            {"i": ["BBB"], "main": ["testA.txt"]},
            {},
        )  # i tag contains a value
        stream4 = Stream(
            streamType.input, "grep", {"main": ["smh"]}, {}
        )  # Invalid File specified
        stream5 = None
        stream6 = Stream(
            streamType.input, "uniq", {"main": ["testA.txt"], "a": []}, {}
        )  # Invalid option tag
        app = Uniq()
        appUnsafe = UniqUnsafe()
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
