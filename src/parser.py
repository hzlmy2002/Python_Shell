from parsita import *


class CommandParsers(TextParsers, whitespace=None):
    single_quoted = "'" >> reg(r"[^\n\r']") << "'"
    backquoted = "`" >> reg(r"[^\n\r`]") << "`"
    double_quoted = (
        '"' >> rep(backquoted | reg(r"[^\n\r\"`]")) << '"' > "".join
    )  # concatenate list returned by rep() into single quote argument
    quoted = single_quoted | backquoted | double_quoted

    unquoted = reg(r"[^\s'\"`;|<>]")

    argument = quoted | unquoted > Argument

    whitespace = reg(r"[ \t]+")
    redirection = (">" & whitespace >> argument) | (
        "<" & whitespace >> argument
    ) > Redirection

    atom = redirection | argument

    call = (
        unquoted
        > AppFactory << whitespace >> rep(redirection << whitespace)
        & argument
        & rep(whitespace >> atom)
    ) > Call

    command = fwd()
    seq = command << ";" >> command
    command.define(call | seq)
