from apps.App import App


class Cat(App):
    def __init__(self) -> None:
        super().__init__()

    def exec(self):
        for argument in self.args:
            with open(argument) as f:
                self.out.append(f.read())
