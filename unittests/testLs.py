import sys

sys.path.insert(1, "../src")

from apps import *
from Stream import *
import unittest, os
import shutil


class testApps(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir("testDir")
        self.cwd = os.getcwd()

    def tearDown(self) -> None:
        os.chdir(self.cwd)
        os.rmdir("testDir")

    def testCdChangeDir(self):
        stream1 = Stream(
            streamType.input, "cd", [], ["testDir"], {"working_dir": self.cwd}
        )
        stream2 = Stream(streamType.input, "cd", [], [".."], {"working_dir": self.cwd})
        cd = Cd()
        cdUnsafe = CdUnsafe()
        os.chdir(self.cwd)
        result1 = cd.exec(stream1)
        result2 = cd.exec(stream2)
        os.chdir(self.cwd)
        result3 = cdUnsafe.exec(stream1)
        result4 = cdUnsafe.exec(stream2)
        self.assertEqual(result1.env, result3.env)
        self.assertEqual(result1.env["working_dir"], self.cwd + "/testDir")
        self.assertEqual(result2.env, result4.env)
        self.assertEqual(result2.env["working_dir"], self.cwd)

    def testCdExceptions(self):
        stream1 = Stream(streamType.input, "cat", [], ["testDir", "smh"], {})
        stream2 = Stream(streamType.input, "cat", ["a"], ["testDir"], {})
        stream3 = Stream(streamType.input, "cat", [], ["smh"], {})
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
            "Invalid number of command line arguments" in cdUnsafe.exec(stream1).args[0]
        )
        self.assertTrue(
            "Invalid number of command line parameters"
            in cdUnsafe.exec(stream2).args[0]
        )
        self.assertTrue("Invalid Directory" in cdUnsafe.exec(stream3).args[0])
        self.assertTrue("No stream to process" in cdUnsafe.exec(stream4).args[0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
