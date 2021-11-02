from apps.App import App
import os

class Cd(App):
    def __init__(self) -> None:
        super().__init__()

    def exec(self):
        if len(self.args) == 0 or len(self.args) > 1:
            raise ValueError("wrong number of command line arguments")
        os.chdir(self.args[0])