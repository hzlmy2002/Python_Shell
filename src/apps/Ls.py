from apps.App import App
import os

class Ls(App):
    def __init__(self) -> None:
        super().__init__()

    def list_directory(self, ls_dir):
        for file in os.listdir(ls_dir):
            if not file.startswith("."):
                self.out.append(file + "\n")

    def exec(self):
        if len(self.args) == 0:
            ls_dir = os.getcwd()
        elif len(self.args) > 1:
            raise ValueError("wrong number of command line arguments")
        else:
            ls_dir = self.args[0]
        self.list_directory(ls_dir)