from apps import *
from Stream import *
from apps import tools

def testCat():
    stream1 = Stream(
        streamType=1,
        app="cat",
        params=[],
        args=["\0/tmp/a", "/tmp/b"],
        env={},
    )
    stream2= Stream(
        streamType=1,
        app="cat",
        params=[],
        args=["\0HelloWorld!\n\0"],
        env={},
    )        
    cat = CatUnsafe(stream1)
    output = cat.exec()
    
    print(output.args[0],end="")

testCat()