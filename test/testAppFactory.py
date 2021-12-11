import sys


sys.path.insert(0, "../src")
from apps.decorators import unsafe
from apps import *
import unittest
from appFactory import AppNotFoundError, appFactory


class TestFactory(unittest.TestCase):
    def test_factory(self):
        appNames = [
            "pwd",
            "head",
            "echo",
            "cat",
            "cd",
            "ls",
            "cut",
            "find",
            "grep",
            "sort",
            "uniq",
            "tail",
        ]
        appFunc = [pwd, head, echo, cat, cd, ls, cut, find, grep, sort, uniq, tail]
        for name, func in zip(appNames, appFunc):
            getApp = appFactory(name)
            getUnsafeApp = appFactory("_" + name)
            self.assertEqual(getApp.__hash__(), func.__hash__())
            # self.assertEqual(getUnsafeApp.__hash__(), unsafe(func).__hash__())

    def test_no_app(self):
        with self.assertRaises(AppNotFoundError):
            appFactory("someapp")


if __name__ == "__main__":
    unittest.main()
