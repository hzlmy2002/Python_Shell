import unittest
from shellParser import parseCommand
from shell import Shell


class TestParser(unittest.TestCase):
    def testArgs(self):
        tree = parseCommand("echo hello world", Shell(""))
        args = tree.getCommands()[0].getArgs()
        self.assertEqual(len(args), 2)
        self.assertEqual(args[0].getArg(), "hello")
        self.assertEqual(args[1].getArg(), "world")

    def testQuotes(self):
        tree = parseCommand("echo 'hello world'", Shell(""))
        args = tree.getCommands()[0].getArgs()
        self.assertEqual(len(args), 1)
        self.assertEqual(args[0].getArg(), "hello world")

    def testRedirectionPath(self):
        tree = parseCommand("echo < test.txt hello world", Shell(""))
        args = tree.getCommands()[0].getArgs()
        self.assertEqual(args[0].getPath(), "test.txt")


if __name__ == "__main__":
    unittest.main()
