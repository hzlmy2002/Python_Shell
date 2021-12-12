import sys

sys.path.insert(0, "../src")
import unittest
from shellOutput import ShellOutput, stdout
import os


class testSOutput(unittest.TestCase):
    def testHelperMethods(self):
        so = ShellOutput(None)
        so.sandbox = [1, 2, 3]
        so.record = 123
        so.cleanBuffer()
        self.assertEqual(so.sandbox, [])
        self.assertEqual(so.getSubstitutedRecord(), 123)
        so.setRedirFileName("name")
        self.assertEqual(so.redirFileName, "name")

    def testMode(self):
        so = ShellOutput(None)
        so.setMode(stdout.std)
        self.assertEqual(so.getMode(), stdout.std)
        so.setMode(stdout.subs)
        self.assertEqual(so.getMode(), stdout.std)  # Doesnt change mode
        self.assertTrue(so.isSubstitution)

    def testWriteStd(self):
        so = ShellOutput(None)
        so.setMode(stdout.std)
        so.isSubstitution = True
        so.write("content")
        self.assertEqual(so.record, "content")

    def testWritePipe(self):
        so = ShellOutput(None)
        so.setMode(stdout.pipe)
        so.write("content")
        self.assertEqual(so.sandbox, ["content"])
        so.write("new_content")
        self.assertEqual(so.sandbox, ["new_content"])

    def isReset(self, so):  # Helper function for testing resets
        self.assertEqual(so.sandbox, [])
        self.assertEqual(so.getMode(), stdout.std)
        self.assertEqual(so.redirFileName, "")

    def testWriteRedir(self):
        so = ShellOutput(None)
        so.setMode(stdout.redir)
        so.setRedirFileName("test1.txt")
        so.write("content")
        with open("test1.txt", "r") as f:
            self.assertEqual(f.read(), "content")
        os.remove("test1.txt")
        self.isReset(so)

    def testWriteUnknown(self):
        so = ShellOutput(None)
        so.setMode("smth")
        with self.assertRaises(Exception):
            so.write("content")

    def testGetBuffer(self):
        so = ShellOutput(None)
        so.mode = stdout.pipe
        so.sandbox = ["content"]
        self.assertEqual(so.getBuffer(), "content")
        so.getBuffer(True)
        self.isReset(so)

    def testGetBufferEmptySandbox(self):
        so = ShellOutput(None)
        so.mode = stdout.pipe
        so.sandbox = []
        self.assertEqual(so.getBuffer(), "")

    def testGetBufferException(self):
        so = ShellOutput(None)
        so.mode = stdout.std
        with self.assertRaises(Exception):
            so.getBuffer()  # Inadequate output mode


if __name__ == "__main__":
    unittest.main()
