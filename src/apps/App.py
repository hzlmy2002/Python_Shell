from Stream import Stream

class App:
    def __init__(self) -> None:
        # Pretty useless for now, may need it further in development
        self.stream = None
        self.args = None

    def setter(self,input_stream):
        self.stream = input_stream
        self.args = self.stream.get_args()
    '''
    def pack_output(self):
        raise NotImplementedError("Please Implement this method")'''
    
    def exec(self):
        #exec should return an output list
        raise NotImplementedError("Please Implement this method")
