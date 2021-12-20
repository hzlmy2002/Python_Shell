import sys

sys.path.insert(0, "../src")
from apps.tools import getLines,toList
from apps.exceptions import InvalidArgumentError,InvalidFileOrDir
from streamForTest import StreamForTest
import unittest
import os

class TestTools(unittest.TestCase):
    def setUp(self) -> None:
        self.testString = "Hello world\nThis is\ntestTools"
        with open("testTools.txt","w") as f:
            f.write(self.testString)
    
    def tearDown(self) -> None:
        os.remove("testTools.txt")
    
    def testGetLine(self):
        testStream = StreamForTest(None,None,None,args=["testTools.txt"])
        self.assertEqual("".join(getLines(testStream)),self.testString)
    
    def testGetLineException(self):
        with self.assertRaises(InvalidArgumentError):
            getLines(StreamForTest(None,None,None,args=[]))
        with self.assertRaises(InvalidFileOrDir):
            getLines(StreamForTest(None,None,None,args=["smh.txt"]))
    
    def testToList(self):
        self.assertListEqual(toList(self.testString),toList(self.testString+"\n"))
        self.assertListEqual(toList(self.testString),["Hello world\n","This is\n","testTools\n"])
    
if __name__ == "__main__":
    unittest.main()
