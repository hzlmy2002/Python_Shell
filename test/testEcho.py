import sys

sys.path.insert(0, "../src")
from appTests import appTests
import unittest
from apps.Echo import echo
from appTests import appTests
from hypothesis import given
from hypothesis import given, strategies as st


class testEcho(appTests):
    def setUp(self) -> None:
        self.setApp(echo, "echo")

    @given(s=st.text().filter(lambda x: "*" not in x))  # No glob
    def testEchoOutput(self, s):
        result1 = self.doOutputTest([s])
        result2 = self.doOutputTest([s], unsafeApp=True)
        self.assertEqual(result1, f"{s}\n")
        self.assertEqual(result1, result2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
