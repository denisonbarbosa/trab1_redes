import time
import os
import socket
import threading
import sys
sys.path.append('../')
from Message import Message


class Peer(object):
    def __init__(self, ip, udp_port, tcp_port) -> None:
        """ Constructor of Peer object

        Args:
            ip (str): IP Address of self
            port (int): Port used
        """
        self.ip = ip
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.peer_cache = dict()
        self.r_log = list()
        self.udp_socket = None
        self.tcp_socket = None

        self.available_ports = list()
        for i in range(10):
            if (5000+i) != self.udp_port:
                self.available_ports.append(5000 + i)

        self.create_udp_socket()
        self.scan_files()

    def create_udp_socket(self) -> None:
        """Creates the udp socket and binds it to the port specified
        """
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udp_socket.bind(('', self.udp_port))

    def create_tcp_socket(self) -> None:
        """Creates the tcp socket and binds it to the port specified
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.bind(('', self.tcp_port))
        self.tcp_socket.listen(5)

    def close_udp_socket(self) -> None:
        """Closes the udp socket
        """
        self.udp_socket.close()

    def close_tcp_socket(self) -> None:
        """Closes the tcp socket
        """
        self.tcp_socket.close()

    def add_peer(self, ip, port) -> None:
        """Add peer to the list of known peers

        Args:
            ip (str): IP of the peer
            port (int): UDP port that the peer listens to
        """
        if ip not in self.peer_cache:
            self.peer_cache[ip] = port

    # Client functions

    def request_userlist(self) -> None:
        """Request for listing all the ips in the network
        """

        for port in self.available_ports:
            request = Message(
                (self.ip, 'broadcast',  self.udp_port, port, '1', None))
            self.send_udp_msg(request, '', port)
            time.sleep(0.1)

    def request_filelist(self) -> None:
        """Request for the filelist of all peers
        """
        if len(self.peer_cache) > 0:
            for item in self.peer_cache.items():
                request = Message(
                    ((self.ip, 'broadcast', self.udp_port, item[1], '2', None)))
                self.send_udp_msg(request, item[0], item[1])
                time.sleep(0.1)
        else:
            print(f'0 peers known. Use ip list first\n')

    def request_filename(self, filename) -> bool:
        """Request for finding specific file

        Args:
            filename (str): Name of the file to be searched
        Returns:
            bool: True if the peer has the file, False otherwise
        """
        if len(self.peer_cache) > 0:
            for item in self.peer_cache.items():
                request = Message(
                    ((self.ip, 'broadcast', self.udp_port, item[1], '3', filename)))
                self.send_udp_msg(request, item[0], item[1])
                time.sleep(0.1)
        else:
            print(f'0 peers known. Use ip list first\n')

    def request_file(self, target_ip, filename) -> None:  # TODO
        """Request for downloading the specified file from the IP

        Args:
            target_ip (str): Peer containing the file
            filename (str): Name of the file to be downloaded
        """
        request = Message(((self.ip, target_ip, self.udp_port,
                          self.peer_cache[target_ip], '4', filename)))
        self.send_udp_msg(request, target_ip, request.d_port)
        time.sleep(0.1)

    # Server functions

    def listen(self) -> None:
        """Listens for requisitions and treats them properly
        """
        while True:
            # Recover the message present in the peer socket
            msg, (addr, port) = self.udp_socket.recvfrom(4096)
            if not msg:
                # If there isn't a message, continues listening
                continue

            msg = msg.decode()
            requisition_list = msg.split()
            requisition = Message(requisition_list)
            self.update_log(requisition)
            response = None

            # RESPONSES
            if requisition.type == 'error':
                print(f'Something went wrong')

            elif requisition.type == '01':  # IP response
                self.add_peer(requisition.source, int(requisition.s_port))
                print(f'{requisition.source}\n')

            elif requisition.type == '02':  # file list response
                # prints the file list received
                for file in requisition.content.split():
                    print(f'{requisition.source} {file}\n')

            elif requisition.type == '03':  # search file response
                # prints the confirmation received
                if requisition.content == 'True':
                    print(f'{requisition.source} has the file\n')
                else:
                    print(f'{requisition.source} does not have the file\n')

            elif requisition.type == '04':  # download file response
                # connects to the server port received
                self.tcp_socket = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                file_rec, c_port = requisition.content.split()
                self.tcp_socket.connect(('', int(c_port)))
                
                # creates the file and write its content
                file = open(file_rec, 'wb')
                f = self.tcp_socket.recv(8192)
                file.write(f)
                file.close()

            # REQUESTS
            elif requisition.type == '1':  # IP requisition
                # sends its ip to the client
                response = Message(
                    (self.ip, addr, self.udp_port, requisition.s_port, '01', self.ip))

            elif requisition.type == '2':  # file list requisition
                # updates its file list
                self.scan_files()
                # sends the file list to the client
                file_list = ' '.join([str(item)
                                      for item in self.file_list])
                response = Message(
                    (self.ip, addr, self.udp_port, requisition.s_port, '02', file_list))

            elif requisition.type == '3':  # search file requistion
                # checks if it has the file 
                status = True if self.find_file(
                    requisition.content) else False
                # sends the result of the check to the client
                response = Message((
                    self.ip, addr,  self.udp_port, requisition.s_port, '03', str(status)))

            if requisition.type == '4':  # download file requisition
                if not self.find_file(requisition.content):
                    # Error if the peer does not have the file
                    response = Message(
                        self.ip, addr,  self.udp_port, requisition.s_port, 'error', 'File not found')
                else:
                    # The peer creates the socket and sends the port to the client
                    self.create_tcp_socket()
                    response = Message(
                        (self.ip, addr, self.udp_port, requisition.s_port, '04', requisition.content + ' ' + str(self.tcp_port)))
                    self.send_udp_msg(
                        response, requisition.source, requisition.s_port)
                    # accepts the connection and send the file content to the client
                    s, addr = self.tcp_socket.accept()
                    file = open(requisition.content, 'rb')
                    s.send(file.read(8196))
                    time.sleep(0.1) # wait a little bit in order to receive the appropriate response
                    s.close()
                    self.close_tcp_socket()

            if response and requisition.type != '4':
                self.send_udp_msg(
                    response, requisition.source, requisition.s_port)

    def send_udp_msg(self, message, dest_ip, dest_port):
        """Build and send a message via UDP

        Args:
            message (Message): message object to send
            dest_ip (str): ip of the receiver
            dest_port (int): port to send the message
        """
        self.udp_socket.sendto(str(message).encode(),
                               (dest_ip, int(dest_port)))

    def scan_files(self) -> list:
        """ Scan for the files in the current directory

        Returns:
            list: list of the files in the directory
        """
        self.file_list = os.listdir()

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
        log_entry = f'{requisition.source} {requisition.type} {time.asctime()}'
        self.r_log.append(log_entry)


if __name__ == '__main__':
    """Controller of the peer
    """
    if len(sys.argv) < 4:
        print('Usage: python Peer.py <ip_addr> <udp_port> <tcp_port>')
        exit()
    peer = Peer(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))

    listen_thread = threading.Thread(target=peer.listen)
    listen_thread.start()

    print(f'Peer -> IP = {peer.ip}\nUDP_PORT = {peer.udp_port}\nTCP_PORT = {peer.tcp_port}')
    while True:
        print(
            f'Commands:\n 1) Request user list\n 2) Request files list\n 3) Find file\n 4) Download file\n 5) Print log\n 6) Quit')
        print(f'Use command 1 first to discover the peers in the network\n')
        option = input()

        if option == '1':    # Request user list
            peer.request_userlist()

        elif option == '2':  # Request files list
            peer.request_filelist()

        elif option == '3':  # Find file
            print(f'Enter the filename:')
            filename = input()
            print(f'Requesting file {filename}')
            peer.request_filename(filename)

        elif option == '4':  # Download file
            ip, filename = input().split()
            print(f'Enter the ip of the peer and the filename\n Usage: <ip> <filename>')
            peer.request_file(ip, filename)

        elif option == '5':  # Print log
            peer.print_log()

        elif option == '6':
            print('Use ctrl+C to interrupt the listening thread\n')
            quit()
        else:
            print(f'option {option} not available')
