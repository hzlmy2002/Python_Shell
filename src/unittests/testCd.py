import sys

sys.path.insert(0, "..")

from apps import *
from apps.Stream import *
import unittest, os
from StreamForTest import StreamForTest
from apps.Exceptions import InvalidArgumentError, InvalidFileOrDir


class testCd(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir("testDir")
        self.cwd = os.getcwd()

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        os.rmdir("testDir")

    def testCdChangeDir(self):
        stream1 = StreamForTest({"workingDir": self.cwd}, None, ["testDir"])
        stream2 = StreamForTest(
            {"workingDir": os.path.join(self.cwd, "testDir")}, None, [".."]
        )
        # cdUnsafe = CdUnsafe()
        cd(stream1)
        result1 = stream1.getEnv("workingDir")
        cd(stream2)
        result2 = stream2.getEnv("workingDir")
        # result3 = cdUnsafe.exec(stream1)
        # result4 = cdUnsafe.exec(stream2)
        # self.assertEqual(result1.env, result3.env)
        self.assertEqual(result1, os.path.join(self.cwd, "testDir"))
        # self.assertEqual(result2.env, result4.env)
        self.assertEqual(result2, self.cwd)

    def testCdExceptions(self):
        # cdUnsafe = CdUnsafe()
        with self.assertRaises(InvalidArgumentError):
            cd(
                StreamForTest({"workingDir": self.cwd}, None, ["testDir", "smh"])
            )  # Too many arguments
        with self.assertRaises(InvalidArgumentError):
            cd(StreamForTest({"workingDir": self.cwd}, None, []))  # No directory
        with self.assertRaises(InvalidFileOrDir):
            cd(
                StreamForTest({"workingDir": self.cwd}, None, ["smh"])
            )  # Not existing directory
        """self.assertTrue(
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
        )"""


if __name__ == "__main__":
    unittest.main(verbosity=2)
