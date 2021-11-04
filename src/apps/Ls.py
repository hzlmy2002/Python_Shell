from apps.App import App
import os


class Ls(App):
    def __init__(self) -> None:
        super().__init__()

    def list_directory(self, ls_dir):
        dirs = []
        for file in os.listdir(ls_dir):
            if not file.startswith("."):
                dirs.append(file + "\n")
        return dirs

    def exec(self):
        if not self.args:
            ls_dir = os.getcwd()
        else:
            ls_dir = self.args[0]
        return self.list_directory(ls_dir)

    """def exec(self):
        if len(self.args) == 0:
            ls_dir = os.getcwd()
        elif len(self.args) > 1:
            raise ValueError("wrong number of command line arguments")
        else:
            ls_dir = self.args[0]
        self.list_directory(ls_dir)
        return self.output"""
