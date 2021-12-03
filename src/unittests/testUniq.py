import sys

sys.path.insert(0, "..")

from apps import *
import unittest, os
from apps.Exceptions import (
    InvalidArgumentError,
    InvalidParamTagError,
    InvalidFileOrDir,
)
from appTests import appTests


class testUniq(unittest.TestCase):
    def setUp(self) -> None:
        with open("testA.txt", "w") as file:
            file.write(
                "Hello Hello\nHELLO HELLO\nHello World\nHelloHello\nHelloHello\nHelloHello\nWorld\nWorld\nWorld"
            )
        with open("testB.txt", "w") as file:
            file.write(
                "Hello Hello\nHELLO HELLO\nHello World\nHelloHello\nHelloHello\nHelloHello\nWorld\nWorld\nWorld\n"
            )
        self.tester = appTests(uniq)

    def tearDown(self) -> None:
        os.remove("testA.txt")
        os.remove("testB.txt")

    def matchHelper(self, result1, result2, stringPattern):
        self.assertEqual(result1, result2)
        self.assertEqual(result1, stringPattern)

    def testUniqFile(self):
        # appUnsafe = UniqUnsafe()
        result1 = self.tester.doOuputTest(["testA.txt"])
        # result2 = appUnsafe.exec(stream)
        result3 = self.tester.doOuputTest(["-i", "testA.txt"])
        # result4 = appUnsafe.exec(stream2)
        result5 = self.tester.doOuputTest(["testB.txt"])
        # result6 = appUnsafe.exec(stream3)
        result7 = self.tester.doOuputTest(["-i", "testB.txt"])
        # result8 = appUnsafe.exec(stream4)
        self.matchHelper(
            result1,
            result1,
            "Hello Hello\nHello World\nHelloHello\nWorld\nWorld",
        )
        self.matchHelper(
            result3,
            result3,
            "Hello Hello\nHELLO HELLO\nHello World\nHelloHello\nWorld\nWorld",
        )
        self.matchHelper(
            result5,
            result5,
            "Hello Hello\nHello World\nHelloHello\nWorld\n",
        )
        self.matchHelper(
            result7,
            result7,
            "Hello Hello\nHELLO HELLO\nHello World\nHelloHello\nWorld\n",
        )

    def testUniqExceptions(self):
        # appUnsafe = UniqUnsafe()
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["testB.txt", "testA.txt"])  # Too many arguments
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest([])  # Empty argument
        with self.assertRaises(InvalidArgumentError):
            self.tester.doOuputTest(["-i", "123", "testA.txt"])  # Too many arguments
        with self.assertRaises(InvalidFileOrDir):
            self.tester.doOuputTest(["-i", "smh"])  # Not existing file
        with self.assertRaises(InvalidParamTagError):
            self.tester.doOuputTest(["-a", "testA.txt"])  # Invalid flag A
        """self.assertTrue(
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
        )"""


if __name__ == "__main__":
    unittest.main(verbosity=2)
