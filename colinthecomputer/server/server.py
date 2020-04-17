import pathlib
import threading

import colinthecomputer.protocol as ptc
from colinthecomputer.parsers import parsers

HEADER_SIZE = 20
run = True


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
        try:
            with self.client:
                # Receive hello
                data = self.client.receive_message()
                if (data == b'kill'):
                    global run
                    run = False
                    return
                user = ptc.User()
                user.ParseFromString(data)
                # Receive snapshot
                data = self.client.receive_message()
                snapshot = ptc.Snapshot()
                snapshot.ParseFromString(data)

            with Handler.lock:
                self.publish((user, snapshot))

        except Exception as error:
            print(f"ERROR in {__name__}: {error}")
            return
 

def print_message(message):
    print(message) 


def run_server(host='127.0.0.1', port=8000, publish=print_message):
    """Run server, which starts a listner and handles 
    every client connection in a new thread.
    
    :param host: server ip address, defaults to '127.0.0.1'
    :type host: str, optional
    :param port: server port, defaults to 8000
    :type port: int, optional
    :param publish: publishing function to incoming snapshots,
    defaults to printing to STDOUT
    :type publish: callable, optional
    """
    # Setup server
    with ptc.Listener(host=host, port=port) as server:
        while run:
            # Recieve message
            client = server.accept()
            handler = Handler(client, publish)
            handler.start()
