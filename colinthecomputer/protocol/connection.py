import socket
import struct

CHUNK = 1000000


class Connection:
    """Incapsulates the network connection to an endpoint,
    providing a connect, send_message and receive_message methods.

    :param socket: the connection socket
    :type socket: socket
    """
    def __init__(self, socket):
        self.socket = socket

    @classmethod
    def connect(cls, host, port):
        """Create a connection object to (host, port), returns None if failed.
        
        :param host: peer host address
        :type host: str
        :param port: peer port
        :type port: int
        :returns: connection to the desired address
        :rtype: Connection
        """
        sock = socket.socket()
        sock.connect((host, port))
        return Connection(sock)

    def __repr__(self):
        lip, lport = self.socket.getsockname()
        rip, rport = self.socket.getpeername()
        return f'<Connection from {lip}:{lport} to {rip}:{rport}>'

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()

    def _receive(self, size):
        """Recieve size bytes from peer.

        :param size: size of required data
        :type size: int
        :returns: received data
        :rtype: byte-string
        :raises RuntimeError: incomplete data error if received less than size bytes
        """
        received = 0
        chunks = []
        while received < size:
            chunk = self.socket.recv(CHUNK)
            received += len(chunk)
            if not chunk:
                raise RuntimeError('incomplete data')
            chunks.append(chunk)
        data = b''.join(chunks)
        return data

    def send_message(self, message):
        """Sends message to peer.
        
        :param message: message to send
        :type message: byte-string
        """
        data = b''
        data += struct.pack('I', len(message))
        data += message
        self.socket.sendall(data)

    def receive_message(self):
        """Receives message from peer.
        
        :returns: the received message
        :rtype: byte-string
        """
        size, = struct.unpack('I', self.socket.recv(4))
        return self._receive(size)

    def close(self):
        self.socket.close()
