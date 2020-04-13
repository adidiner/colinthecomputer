from .connection import Connection
import socket


class Listener:
    """A connection listener, listening to and accepting connections.
    
    :param port: listener port
    :type port: number
    :param host: listener host address, defaults to '0.0.0.0'
    :type host: str, optional
    :param backlog: listem backlog, defaults to 1000
    :type backlog: number, optional
    :param reuseaddr: whehter to enable reuseaddr, defaults to True
    :type reuseaddr: bool, optional
    """
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
        """Start listening on (self.host,self.port)
        """
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.backlog)

    def stop(self):
        """Stop listening"""
        self.socket.close()

    def accept(self):
        """Accept a new connection"""
        return Connection(self.socket.accept()[0])
