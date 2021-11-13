from apps.App import App
import os


class Pwd(App):
    def __init__(self) -> None:
        super().__init__()

    def exec(self, stream: "Stream") -> "Stream":
        self.stream = stream
        return [os.getcwd() + "\n"]
