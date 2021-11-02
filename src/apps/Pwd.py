from apps.App import App
import os

class Pwd(App):
    def __init__(self) -> None:
        super().__init__()

    def exec(self):
        self.out.append(os.getcwd())