import re
from glob import glob
from Stream import Stream


class Parser:
    def __init__(self) -> None:
        pass

    def setup_stream(self, tokens, env):
        # Current setup includes the parameters into arguments
        application = tokens[0]
        arguments = tokens[1:]
        return Stream(1, application, None, arguments, env)

    def parse_token(self, command):
        # Separates command into list [app,args] and returns it
        tokens = []
        for m in re.finditer("[^\\s\"']+|\"([^\"]*)\"|'([^']*)'", command):
            if m.group(1) or m.group(2):
                quoted = m.group(0)
                tokens.append(quoted[1:-1])
            else:
                globbing = glob(m.group(0))
                if globbing:
                    tokens.extend(globbing)
                else:
                    tokens.append(m.group(0))
        return tokens

    def parse(self, raw_command, env):
        command_list = []
        for com in raw_command:
            tokens = self.parse_token(com)
            command_list.append(self.setup_stream(tokens, env))
        return command_list
