import re
from glob import glob
from Stream import Stream


class Parser:
    def __init__(self) -> None:
        pass

    def setup_stream(self, tokens):
        # Current setup includes the parameters into arguments
        application = tokens[0]
        arguments = tokens[1:]
        return Stream(1, application, None, arguments, None)

    def parse_token(self, command):
        # Separates command into a token (list [app,args]) and returns it
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

    def parse(self, sing_com):
        # Packs input singular command into an stream object
        tokens = self.parse_token(sing_com)
        return self.setup_stream(tokens)
