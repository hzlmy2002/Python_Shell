import sys

sys.path.insert(0, "..")

from apps import *
import unittest, os
from apps.Exceptions import InvalidArgumentError, InvalidParamTagError, InvalidFileOrDir
from appTests import appTests


class testHead(unittest.TestCase):
    def setUp(self) -> None:
        self.tester = appTests(head)
        with open("test.txt", "w") as file:
            file.write("l1\nl2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\n")

    def tearDown(self) -> None:
        os.remove("test.txt")

    def testHeadFile(self):
        # appUnsafe = HeadUnsafe()
        result1 = self.tester.doOuputTest(["test.txt"])
        # result2 = headUnsafe.exec(stream1)
        result3 = self.tester.doOuputTest(["-n", "11", "test.txt"])
        # result4 = headUnsafe.exec(stream2)
        # self.assertEqual(result1.params["main"][0], result2.params["main"][0])
        self.assertEqual(result1, "l1\nl2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\n")
        # self.assertEqual(result3.params["main"][0], result4.params["main"][0])
        self.assertEqual(result3, "l1\nl2\nl3\nl4\nl5\nl6\nl7\nl8\nl9\nl10\nl11\n")

    """def testHeadStdin(self):
        stream = Stream(
            streamType.input,
            "head",
            {"n": [], "main": [tools.str2stdin("Hello World!\n")]},
            {},
        )
        app = Head()
        appUnsafe = HeadUnsafe()
        result1 = app.exec(stream)
        result2 = appUnsafe.exec(stream)
        self.assertEqual(result1.params["main"], result2.params["main"])
        self.assertEqual(result1.params["main"][0], "Hello World!\n")"""

    def testHeadExceptions(self):
        # headUnsafe = HeadUnsafe()
        with self.assertRaises(InvalidParamTagError):
            self.tester.doOuputTest(["-a", "11", "test.txt"])  # Invalid param tag -a
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(
                ["-n", "11", "test.txt", "smh"]
            )  # Way to many arguments
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest(["-n", "11", "smh.txt"])  # Not existing file
        """self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum)
            in headUnsafe.exec(stream1).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramType)
            in headUnsafe.exec(stream2).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.argNum)
            in headUnsafe.exec(stream3).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.paramNum)
            in headUnsafe.exec(stream4).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.file)
            in headUnsafe.exec(stream5).params["main"][0]
        )
        self.assertTrue(
            msg.exceptionMsg(exceptionType.none)
            in headUnsafe.exec(stream6).params["main"][0]
        )"""


if __name__ == "__main__":
    unittest.main(verbosity=2)
