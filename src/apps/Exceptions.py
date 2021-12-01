class MissingParamError(RuntimeError):
    pass


class InvalidParamTagError(RuntimeError):
    pass


class InvalidArgumentError(RuntimeError):
    pass


class InvalidFileOrDir(FileNotFoundError):
    pass
