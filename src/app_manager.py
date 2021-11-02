from collections import defaultdict
from apps import *


def def_val():
    raise ValueError("unsupported application")


class AppManager:
    def __init__(self) -> None:
        self.app_map = defaultdict(def_val)
        self.app_map["pwd"] = Pwd()
        self.app_map["echo"] = Echo()
        self.app_map["cd"] = Cd()
        self.app_map["cat"] = Cat()
        self.app_map["ls"] = Ls()
        self.app_map["head"] = Head()
        self.app_map["tail"] = Tail()
        self.app_map["grep"] = Grep()
        self.app_map["cut"] = Cut()
        self.app_map["find"] = Find()
        self.app_map["uniq"] = Uniq()
        self.app_map["sort"] = Sort()

    def extract_app(self, token, out, args):
        """Returns app class corresponding to the string token"""
        self.app_map[token].setter(out, args)
        return self.app_map[token]
