from parsita import *
from command_tree import Argument, InRedirection, OutRedirection, Call, Seq
from app_factory import CommandNotFoundError, app_factory
from apps.App import App


class CommandParsers(TextParsers, whitespace=None):
    single_quoted = "'" >> reg(r"[^\n\r']") << "'"
    backquoted = "`" >> reg(r"[^\n\r`]") << "`"
    double_quoted = (
        '"' >> rep("`" & reg(r"[^\n\r`]") & "`" | reg(r"[^\n\r\"`]")) << '"' > "".join
    )  # concatenate list returned by rep() into single quote string
    quoted = single_quoted | backquoted | double_quoted

    unquoted = reg(r"[^\s'\"`;|<>]")

    argument = (quoted | unquoted) > Argument

    whitespace = reg(r"[ \t]+")
    in_redirection = (">" >> whitespace >> argument) > InRedirection
    out_redirection = ("<" >> whitespace >> argument) > OutRedirection
    redirection = in_redirection | out_redirection

    atom = argument | redirection

    def get_app(app_name: str) -> Parser[str, "App"]:
        try:
            app = app_factory(app_name)
            return success(app)
        except CommandNotFoundError as e:
            return failure("Command {app_name} not found.")

    call = (
        unquoted
        >= get_app << whitespace >> rep(redirection << whitespace)
        & argument
        & rep(whitespace >> atom)
    ) > Call

    command = fwd()
    seq = (command << ";" >> command) > Seq
    command.define(call | seq)
