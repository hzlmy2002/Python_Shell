"""
for dignose only, ignore this file
"""


from apps import Cat
from apps.Stream import *
from apps import tools
def test():
    s1=Stream(sType=streamType.input, app="", params={"main": [tools.str2stdin("asdf"),"asdfasdf"]}, env={})
    cat=Cat()
    out=cat.exec(s1)
    print(out.params["main"][-1])
    pass

test()
