from collections import defaultdict
from apps import *


def def_val():
    raise ValueError("unsupported application")


class AppManager:
    def __init__(self) -> None:
        self.appMap = defaultdict(def_val)
        self.appMap["pwd"] = Pwd()
        self.appMap["echo"] = Echo()
        self.appMap["cd"] = Cd()
        self.appMap["cat"] = Cat()
        self.appMap["_cat"]= CatUnsafe()
        self.appMap["ls"] = Ls()
        self.appMap["head"] = Head()
        self.appMap["tail"] = Tail()
        self.appMap["grep"] = Grep()
        self.appMap["cut"] = Cut()
        self.appMap["find"] = Find()
        self.appMap["uniq"] = Uniq()
        self.appMap["sort"] = Sort()

    def runApp(self, command_list):
        """Returns list of output stream"""
        output_list = []
        for stream in command_list:
            app = self.appMap[stream.get_app()]
            # Setup application parameters for the new stream
            app.setter(stream)
            output_list += app.exec()
        return output_list
