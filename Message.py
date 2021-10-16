class Message(object):
    def __init__(self, args) -> None:
        """Constructor of a Message object

        Args:
            args (list(str)): List of arguments needed
            [0] -> source_ip
            [1] -> dest_ip
            [2] -> source_port
            [3] -> dest_port
            [4] -> message_type
            [5] -> content
        """
        self.source = args[0]
        self.destination = args[1]
        self.s_port = args[2]
        self.d_port = args[3]
        self.type = args[4]
        self.content = ' '.join(str(i) for i in args[5:])

    def __str__(self):
        return f'{self.source} {self.destination} {self.s_port} {self.d_port} {self.type} {self.content}'
