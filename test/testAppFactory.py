import sys

sys.path.insert(0, "../src")
from appFactory import AppNotFoundError, appFactory
import unittest
from apps import cat, cd, cut, echo, find, grep, head, ls, pwd, sort, tail, uniq


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
        appFunc = [
            pwd.pwd,
            head.head,
            echo.echo,
            cat.cat,
            cd.cd,
            ls.ls,
            cut.cut,
            find.find,
            grep.grep,
            sort.sort,
            uniq.uniq,
            tail.tail,
        ]
        for name, func in zip(appNames, appFunc):
            getApp = appFactory(name)
            self.assertEqual(getApp.__hash__(), func.__hash__())
            # self.assertEqual(getUnsafeApp.__hash__(),unsafe(func).__hash__())

    def test_no_app(self):
        with self.assertRaises(AppNotFoundError):
            appFactory("someapp")


if __name__ == "__main__":
    unittest.main()
