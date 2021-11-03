from apps.HeadTail import HeadTail

class Tail(HeadTail):
    def __init__(self) -> None:
        super().__init__()

    def file_op(self, lines):
        display_length = min(len(lines), self.num_lines)
        for i in range(0, display_length):
            self.output.append(lines[len(lines) - display_length + i])