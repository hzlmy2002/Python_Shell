from apps import *


class AppNotFoundError(RuntimeError):
    pass


appMap = {}
appMap["pwd"] = Pwd()
appMap["echo"] = Echo()
appMap["cd"] = Cd()
appMap["cat"] = Cat()
appMap["_cat"] = CatUnsafe()
appMap["ls"] = Ls()
appMap["head"] = Head()
appMap["tail"] = Tail()
appMap["grep"] = Grep()
appMap["cut"] = Cut()
appMap["find"] = Find()
appMap["uniq"] = Uniq()
appMap["sort"] = Sort()


def getApp(app_name):
    try:
        app = appMap[app_name]
    except KeyError:
        raise AppNotFoundError("Application not found.")
    return app
