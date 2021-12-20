class MissingParamError(RuntimeError):
    pass


class InvalidParamError(RuntimeError):
    pass


class InvalidParamTagError(RuntimeError):
    pass


class InvalidArgumentError(RuntimeError):
    pass


class InvalidFileOrDir(FileNotFoundError):
    pass


class MissingStdin(RuntimeError):
    pass
