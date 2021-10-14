import os
import socket
import threading
import sys
import Message


class Peer(object):
    def __init__(self, ip, port) -> None:
        """ Constructor of Peer object

        Args:
            ip (str): IP Address of self
            port (int): Port used
        """
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.bind((self.ip, self.port))
        self.socket.listen(1)
        self.scan_files()

    # Client functions
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

    # Server functions

    def listen(self) -> None:
        """Listens for requisitions and treats them properly
        """
        while True:
            sckt, addr = self.socket.accept()
            requisition_list = sckt.recv(1024).decode().split()
            requisition = Message.Message(requisition_list)

            if requisition.type == 1:  # IP requisition
                response = self.ip
                self.socket.send(response.encode())

            if requisition.type == 2:  # file list requisition
                self.scan_files()
                response = str(self.file_list())
                self.socket.send(response.encode())

            if requisition.type == 3:  # search file requistion
                if self.find_file(requisition.content):
                    response = True
                else:
                    response = False
                self.socket.send(response.encode())

            if requisition.type == 4:  # download file requisition
                pass

    def scan_files(self) -> list:
        """ Scan for the files in the current directory

        Returns:
            list: list of the files in the directory
        """
        self.file_list = os.listdir()

    def get_port(self) -> int:
        """ Getter for the ip

        Returns:
            str: IP Address of self
        """
        return self.port

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


if __name__ == '__main__':
    peer = Peer(str(sys.argv[1]), 139)

    listen_thread = threading.Thread(None, peer.listen())
    listen_thread.run()
    while True:

        print(f'Commands:\n 1) Request user list\n 2) Request files list\n 3) Find file\n 4) Download file')
        option = int(input())

        if option == 1:
            pass
        elif option == 2:
            pass
        elif option == 3:
            pass
        elif option == 4:
            pass
