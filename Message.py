class Message(object):
    def __init__(self, args) -> None:
        self.source = args[0]
        self.destination = args[1]
        self.type = args[2]
        self.content = args[3]
