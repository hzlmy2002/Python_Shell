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

    def run_app(self, command_list):
        """Returns list of output stream"""
        output_list = []
        for stream in command_list:
            app = self.app_map[stream.get_app()]
            # Setup application parameters for the new stream
            app.setter(stream)
            output_list += app.exec()
        return output_list
