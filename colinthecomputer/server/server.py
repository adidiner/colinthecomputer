import pathlib
import threading

from colinthecomputer.protocol import Listener
from colinthecomputer.parsers import run_parser
from colinthecomputer.parsers import parsers
from colinthecomputer.protocol import User, Config, Snapshot


HEADER_SIZE = 20


class Handler(threading.Thread):
    """Handels a single connection from client.

    :param client: client connection
    :type client: Connection
    :param publish: publishing function (for client message)
    :type publish: callable
    """
    lock = threading.Lock()

    def __init__(self, client, publish):
        super().__init__()
        self.client = client
        self.publish = publish

    def run(self):
        """Run handler, communicating in hello -> condif -> snapshot protocol.
        Use self.publish to publish the snapshot. 
        """
        with self.client:
            # Receive hello
            data = self.client.receive_message()
            user = User()
            user.ParseFromString(data)
            # Send config
            config = Config(fields=parsers.keys())
            data = config.SerializeToString()
            self.client.send_message(data)
            # Receive snapshot
            data = self.client.receive_message()
            snapshot = Snapshot()
            snapshot.ParseFromString(data)

        # TODO: figure out exception handling
        with Handler.lock:
            self.publish((user, snapshot))
        


def run_server(host, port, publish):
    """Run server, which starts a listner and handles 
    every client connection in a new thread.
    
    :param host: server ip address
    :type host: str
    :param port: server port
    :type port: int
    :param publish: publishing function to incoming snapshots
    :type publish: callable
    """
    # Setup server
    with Listener(host=host, port=port) as server:
        while True:
            # Recieve message
            client = server.accept()
            handler = Handler(client, publish)
            handler.start()
