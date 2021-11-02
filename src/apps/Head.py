from apps.HeadTail import HeadTail

class Head(HeadTail):
    def __init__(self) -> None:
        super().__init__()

    def file_op(self, lines):
        for i in range(0, min(len(lines), self.num_lines)):
            self.out.append(lines[i])