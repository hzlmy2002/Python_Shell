from apps import *


class AppNotFoundError(RuntimeError):
    pass


class appFactory:
    def __init__(self):
        self.appMap = {}
        self.appMap["pwd"] = Pwd()
        self.appMap["echo"] = Echo()
        self.appMap["cd"] = Cd()
        self.appMap["cat"] = Cat()
        self.appMap["_cat"] = CatUnsafe()
        self.appMap["ls"] = Ls()
        self.appMap["head"] = Head()
        self.appMap["tail"] = Tail()
        self.appMap["grep"] = Grep()
        self.appMap["cut"] = Cut()
        self.appMap["find"] = Find()
        self.appMap["uniq"] = Uniq()
        self.appMap["sort"] = Sort()

    def get(self, app_name):
        if app_name in self.appMap:
            return self.appMap[app_name]
        else:
            raise AppNotFoundError(app_name)


def test():
    af = appFactory().get("pwd")
    pass


test()
