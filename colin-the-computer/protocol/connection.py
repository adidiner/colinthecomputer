import socket
import struct

CHUNK = 1000000


class Connection:
    def __init__(self, socket):
        self.socket = socket

    @classmethod
    def connect(cls, host, port):
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
        data = b''
        while len(data) < size:
            received = self.socket.recv(CHUNK)
            if not received:
                print('oof')  # TODO
                continue
            data += received
        return data

    def send_message(self, message):
        data = b''
        data += struct.pack('I', len(message))
        data += message
        self.socket.sendall(data)

    def receive_message(self):
        size, = struct.unpack('I', self.socket.recv(4))
        return self._receive(size)

    def close(self):
        self.socket.close()
