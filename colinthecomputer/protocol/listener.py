from .connection import Connection
import socket


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr
        self.socket = socket.socket()
        if self.reuseaddr:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __repr__(self):
        return f'Listener(port={self.port!r}, host={self.host!r}, ' \
               f'backlog={self.backlog!r}, reuseaddr={self.reuseaddr!r})'

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exception, error, traceback):
        self.stop()

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.backlog)

    def stop(self):
        self.socket.close()

    def accept(self):
        return Connection(self.socket.accept()[0])
