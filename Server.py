import os


class Server:
    def __init__(self, ip) -> None:
        """ Constructor of Peer object

        Args:
            ip (str): IP Address of self
        """
        self.ip = ip
        self.scan_files()
        self.r_log = list()

    def scan_files(self) -> list:
        """ Scan for the files in the current directory

        Returns:
            list: list of the files in the directory
        """
        self.file_list = os.listdir()

    def get_ip(self) -> str:
        """ Getter for the ip

        Returns:
            str: IP Address of self
        """
        return self.ip

    def find_file(self, filename) -> bool:
        """Checks if the Peer contains the file

        Args:
            filename (str): name of the file to be searched

        Returns:
            bool: True if the file is found, False otherwise
        """
        if filename in self.file_list:
            return True
        return False

    def send_file(self, filename) -> bool:
        pass

    def print_log(self) -> None:
        """Prints the requisitions log
        """
        for r in self.r_log:
            print(r)

    def update_log(self, requisition) -> None:
        """Adds the requisition to the log

        Args:
            requisition (Requisition): requisition to be saved in the log
        """
        self.r_log.append(requisition)
