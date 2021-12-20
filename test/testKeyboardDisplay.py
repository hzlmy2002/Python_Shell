import sys

sys.path.insert(0, "../src")
from keyboardDisplay import Data, State
import unittest


class testKeyboardDisplay(unittest.TestCase):
    def testData(self):
        d = Data()
        print(d)
        d.pressUp()
        self.assertEqual(d.isUpPressed(), True)
        d.pressUp()
        self.assertEqual(d.isUpPressed(), False)
        d.add("a")
        self.assertEqual(d.get(), "a")
        d.update("b")
        self.assertEqual(d.get(), "b")
        d.addHistory()
        self.assertEqual(d.getHistory(), ["b"])
        d.setPrefix("c")
        self.assertEqual(d.getWithPrefix(), "cb ◄")
        d.add("d")
        self.assertEqual(d.getWithPrefix(), "cbd ◄")
        d.update("e")
        self.assertEqual(d.getWithPrefix(), "ce ◄")
        d.addHistory()
        d.setCounter(2)
        self.assertEqual(d.getHistory(), ["b", "e"])
        self.assertEqual(d.getCounter(), 2)
        d.setCounter(0)
        d.pop()
        self.assertEqual(d.get(), "")
        d.clear()
        self.assertEqual(d.getWithPrefix(), "c")

    def testState(self):
        s = State()
        self.assertEqual(s.alive, True)
        s.die()
        self.assertEqual(s.alive, False)
        s.die()
        self.assertEqual(s.alive, False)


if __name__ == "__main__":
    unittest.main(verbosity=2)
