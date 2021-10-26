from collections import defaultdict
from apps import echo, pwd, cd, cat, ls, head, tail, grep, cut, find, uniq, sort


def def_val():
    raise ValueError("unsupported application")


class appManager:
    def __init__(self) -> None:
        self.app_map = defaultdict(def_val)
        self.app_map["pwd"] = pwd()
        self.app_map["echo"] = echo()
        self.app_map["cd"] = cd()
        self.app_map["cat"] = cat()
        self.app_map["ls"] = ls()
        self.app_map["head"] = head()
        self.app_map["tail"] = tail()
        self.app_map["grep"] = grep()
        self.app_map["cut"] = cut()
        self.app_map["find"] = find()
        self.app_map["uniq"] = uniq()
        self.app_map["sort"] = sort()

    def extract_app(self, token):
        """Returns app class corresponding to the string token"""
        return self.app_map[token]
