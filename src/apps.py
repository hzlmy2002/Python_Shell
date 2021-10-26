import os
from os import listdir
import re


class app:
    def exec(self, out, args):
        raise NotImplementedError("Please Implement this method")


class echo(app):
    def exec(self, out, args):
        out.append(" ".join(args) + "\n")


class pwd(app):
    def exec(self, out, args):
        out.append(os.getcwd())


class cd(app):
    def exec(self, out, args):
        if len(args) == 0 or len(args) > 1:
            raise ValueError("wrong number of command line arguments")
        os.chdir(args[0])


class cat(app):
    def exec(self, out, args):
        for argument in args:
            with open(argument) as f:
                out.append(f.read())


class ls(app):
    def list_directory(self, ls_dir, out):
        for file in listdir(ls_dir):
            if not file.startswith("."):
                out.append(file + "\n")

    def exec(self, out, args):
        if len(args) == 0:
            ls_dir = os.getcwd()
        elif len(args) > 1:
            raise ValueError("wrong number of command line arguments")
        else:
            ls_dir = args[0]
        self.list_directory(ls_dir, out)


class headTail(app):
    def __init__(self):
        self.num_lines = None

    def file_op(self, lines, out):
        """Requires implementation of child class"""
        raise NotImplementedError("Please Implement this method")

    def process_args(self, args):
        """Process arguments passed and returns the name of the file"""
        if len(args) == 1:
            self.num_lines = 10
            return args[0]
        if len(args) == 3:
            if args[0] != "-n":
                raise ValueError("wrong flags")
            self.num_lines = int(args[1])
            return args[2]
        raise ValueError("wrong number of command line arguments")

    def exec(self, out, args):
        file = self.process_args(args)
        with open(file) as f:
            lines = f.readlines()
            self.file_op(lines, out)


class head(headTail):
    def file_op(self, lines, out):
        for i in range(0, min(len(lines), self.num_lines)):
            out.append(lines[i])


class tail(headTail):
    def file_op(self, lines, out):
        display_length = min(len(lines), self.num_lines)
        for i in range(0, display_length):
            out.append(lines[len(lines) - display_length + i])


class grep(app):
    def __init__(self) -> None:
        self.pattern = None
        self.files = None

    def match_line(self, out, filename):
        """Finds matching pattern given by args and append to output"""
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                if re.match(self.pattern, line) and len(self.files) <= 1:
                    out.append(line)
                else:
                    out.append(f"{filename}:{line}")

    def exec(self, out, args):
        if len(args) < 2:
            raise ValueError("wrong number of command line arguments")
        self.pattern = args[0]
        self.files = args[1:]
        for filename in self.files:
            self.match_line(out, filename)


class cut(app):
    def exec(self, out, args):
        pass


class find(app):
    def exec(self, out, args):
        pass


class uniq(app):
    def exec(self, out, args):
        pass


class sort(app):
    def exec(self, out, args):
        pass
