from io import StringIO
from parsita import reg, success, TextParsers, rep, opt, rep1sep, longest, rep1
from commandTree import Argument, InRedirection, OutRedirection, Call, Pipe, Seq
from appFactory import appFactory


def parseCommand(cmdline: str, shell):
    class CommandParsers(TextParsers, whitespace=None):
        def substitution(subcmd: str):
            stdout = StringIO()
            shell.eval(subcmd, stdout)
            return stdout.getvalue()[:-1]

        singleQuoted = "'" >> reg(r"[^\n\r']*") << "'"
        backQuoted = "`" >> reg(r"[^\n\r`]*") << "`" > substitution
        doubleQuoted = '"' >> rep(backQuoted | reg(r"[^\n\r\"`]+")) << '"' > "".join
        quoted = singleQuoted | backQuoted | doubleQuoted

        unquoted = reg(r"[^\s'\"`;|<>]+")

        argument = (rep1(quoted | unquoted) > "".join) > Argument

        whitespace = reg(r"[ \t]+")
        inRedirection = ("<" >> opt(whitespace) >> argument) > InRedirection
        outRedirection = (">" >> opt(whitespace) >> argument) > OutRedirection
        redirection = inRedirection | outRedirection

        atom = redirection | argument

        def makeCall(args) -> "Call":
            redirections = args[0]
            appName = args[1].getArg()
            atoms = args[2]

            app = appFactory(appName)
            mergedArgs = redirections + atoms  # merge sublists generated by combinator
            return Call(app, mergedArgs)

        call = (
            (opt(whitespace) >> rep(redirection << whitespace))
            & argument
            & (rep(whitespace >> atom) << opt(whitespace))
        ) > makeCall

        pipe = rep1sep(call, "|") > Pipe
        command = rep1sep(longest(call, pipe), ";") > Seq

    return CommandParsers.command.parse(cmdline).or_die()
