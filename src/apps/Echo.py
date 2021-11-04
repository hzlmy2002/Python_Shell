from apps.App import App


class Echo(App):
    def __init__(self) -> None:
        super().__init__()

    def exec(self):
        output = " ".join(self.args) + "\n"
        return [output]
