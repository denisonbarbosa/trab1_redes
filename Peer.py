import os
import Server
import Client


class Peer(Server, Client):
    def __init__(self, ip) -> None:
        """ Constructor of Peer object

        Args:
            ip (str): IP Address of self
        """
        self.ip = ip
        self.scan_files()
