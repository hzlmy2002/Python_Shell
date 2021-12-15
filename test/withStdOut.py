import unittest
import io
import sys
from shell import Shell


class withStdOut(unittest.TestCase):
    def assertOutput(self, cmd, result, cwd="", ignoreOrder=False):
        output = self.getStdOut(cmd, cwd).strip()
        if ignoreOrder:
            self.assertEqual(set(result.split()), set(output.split()))
        else:
            self.assertEqual(result, output)

    def getStdOut(self, cmdLine, cwd):
        sh = Shell(cwd)
        old = sys.stdout
        new = io.StringIO()
        sys.stdout = new
        sh.eval(cmdLine, new)
        output = new.getvalue()
        sys.stdout = old
        return output
