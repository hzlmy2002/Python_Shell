import os
from os import listdir
import re


class App:
    def __init__(self) -> None:
        # Pretty useless for now, may need it further in development
        self.out = None
        self.args = None

    def setter(self, out, args):
        self.out = out
        self.args = args

    def exec(self):
        raise NotImplementedError("Please Implement this method")


class Echo(App):
    def __init__(self) -> None:
        super().__init__()

    def exec(self):
        self.out.append(" ".join(self.args) + "\n")


class Pwd(App):
    def __init__(self) -> None:
        super().__init__()

    def exec(self):
        self.out.append(os.getcwd())


class Cd(App):
    def __init__(self) -> None:
        super().__init__()

    def exec(self):
        if len(self.args) == 0 or len(self.args) > 1:
            raise ValueError("wrong number of command line arguments")
        os.chdir(self.args[0])


class Cat(App):
    def __init__(self) -> None:
        super().__init__()

    def exec(self):
        for argument in self.args:
            with open(argument) as f:
                self.out.append(f.read())


class Ls(App):
    def __init__(self) -> None:
        super().__init__()

    def list_directory(self, ls_dir):
        for file in listdir(ls_dir):
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


class HeadTail(App):
    def __init__(self):
        super().__init__()
        self.num_lines = None

    def file_op(self, lines):
        """Requires implementation of child class"""
        raise NotImplementedError("Please Implement this method")

    def process_args(self) -> int:
        """Process arguments passed and returns index in args of which file name is stored"""
        if len(self.args) == 1:
            self.num_lines = 10
            return 0
        if len(self.args) == 3:
            if self.args[0] != "-n":
                raise ValueError("wrong flags")
            self.num_lines = int(self.args[1])
            return 2
        raise ValueError("wrong number of command line arguments")

    def exec(self):
        file = self.args[self.process_args()]
        with open(file) as f:
            lines = f.readlines()
            self.file_op(lines)


class Head(HeadTail):
    def __init__(self) -> None:
        super().__init__()

    def file_op(self, lines):
        for i in range(0, min(len(lines), self.num_lines)):
            self.out.append(lines[i])


class Tail(HeadTail):
    def __init__(self) -> None:
        super().__init__()

    def file_op(self, lines):
        display_length = min(len(lines), self.num_lines)
        for i in range(0, display_length):
            self.out.append(lines[len(lines) - display_length + i])


class Grep(App):
    def __init__(self) -> None:
        super().__init__()

    def match_line(self, filename, filelen, pattern):
        """Finds matching pattern given by args and Append to output"""
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                if re.match(pattern, line) and filelen <= 1:
                    self.out.append(line)
                else:
                    self.out.append(f"{filename}:{line}")

    def exec(self):
        if len(self.args) < 2:
            raise ValueError("wrong number of command line arguments")
        pattern = self.args[0]
        files = self.args[1:]
        filelen = len(files)
        for filename in files:
            self.match_line(filename, filelen, pattern)


class Cut(App):
    def exec(self):
        pass


class Find(App):
    def exec(self):
        pass


class Uniq(App):
    def exec(self):
        pass


class Sort(App):
    def exec(self):
        pass
