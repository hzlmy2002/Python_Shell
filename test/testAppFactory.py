from appFactory import AppNotFoundError, appFactory
import unittest
from apps import Cat, Cd, Cut, Echo, Find, Grep,\
    Head, Ls, Pwd, Sort, Tail, Uniq
import sys


sys.path.insert(0, "../src")


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
        appFunc = [Pwd.pwd, Head.head, Echo.echo, Cat.cat, Cd.cd, Ls.ls,
                   Cut.cut, Find.find, Grep.grep, Sort.sort, Uniq.uniq,
                   Tail.tail]
        for name, func in zip(appNames, appFunc):
            getApp = appFactory(name)
            self.assertEqual(getApp.__hash__(), func.__hash__())
            # self.assertEqual(getUnsafeApp.__hash__(),unsafe(func).__hash__())

    def test_no_app(self):
        with self.assertRaises(AppNotFoundError):
            appFactory("someapp")


if __name__ == "__main__":
    unittest.main()
