from apps.App import App


class Cat(App):
    def __init__(self) -> None:
        super().__init__()

    def exec(self):
        output = []
        for argument in self.args:
            with open(argument) as f:
                output.append(f.read())
        return output

