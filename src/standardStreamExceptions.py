from typing import List


class standardStreamExceptions:
    def __init__(self, appname) -> None:
        self.appname = appname

    def notNoneCheck(self, stream):
        if stream == None:
            raise Exception(f"{self.appname}: No stream to process")

    def lenCheck(
        self,
        checkList: "List",
        type: "str",
        notEmpty=False,
        empty=False,
        equalOne=False,
    ):
        length = len(checkList)

        if (
            (notEmpty and length == 0)
            or (empty and length != 0)
            or (equalOne and length != 1)
        ):
            raise Exception(f"{self.appname}: Invalid number of command line {type}")

    def argsLenCheck(
        self, checkList: "List", notEmpty=False, empty=False, equalOne=False
    ):
        self.lenCheck(checkList, "arguments", notEmpty, empty, equalOne)

    def paramsLenCheck(
        self, checkList: "List", notEmpty=False, empty=False, equalOne=False
    ):
        self.lenCheck(checkList, "parameters", notEmpty, empty, equalOne)
