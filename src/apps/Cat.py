from apps.App import App


class Cat(App):
    def __init__(self) -> None:
        super().__init__()

    def exec(self):
        output = []
        for argument in self.args:
            with open(argument) as f:
                line = f.read()
                if not line.endswith("\n"):
                    line += "\n"
                output.append(line)
        print(output)
        return output
