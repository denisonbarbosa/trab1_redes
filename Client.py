class Client:
    def __init__(self, ip) -> None:
        """ Constructor of Peer object

        Args:
            ip (str): IP Address of self
        """
        self.ip = ip
        self.scan_files()

    def request_userlist(self) -> None:
        """Request for listing all the ips in the network
        """
        pass

    def request_filelist(self) -> None:
        """Request for the filelist of all peers
        """
        pass

    def request_filename(self, filename) -> bool:
        """Request for finding specific file

        Args:
            filename (str): Name of the file to be searched
        Returns:
            bool: [description]
        """
        pass

    def request_file(self, target_ip, filename) -> None:
        """Request for downloading the specified file from the IP

        Args:
            target_ip (str): Peer containing the file
            filename (str): Name of the file to be downloaded
        """
        pass
