import pathlib
import threading
import os
import numpy as np

import colinthecomputer.protocol as ptc
from colinthecomputer.parsers import parsers
from colinthecomputer.utils import printerr

HEADER_SIZE = 20
DIRECTORY = os.environ['BLOB_DIR'] + '/raw_data'
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

    @printerr
    def run(self):
        """Run handler, communicating in hello -> config -> snapshot protocol.
        Use self.publish to publish the snapshot, 
        when converting to json before publishing.
        BLOBS are stored in the fs, with only their path being published.
        """
        with self.client:
            # Receive hello
            data = self.client.receive_message()
            # Sometimes I just want to easily kill the server,
            # this is not an infosec course
            if data == b'kill':
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
            user_id = user.user_id
            # Save BLOBs to filesystem
            path = pathlib.Path(DIRECTORY) / str(user_id) / str(snapshot.datetime)
            _save_binary(path, snapshot)

            # Create slim to-publish json messages
            user = ptc.json_user_message(user)
            snapshot = ptc.json_snapshot_message(snapshot, user_id, path)
            self.publish((user, snapshot))



@printerr
def run_server(host='0.0.0.0', port=8000, publish=print):
    """Run server, which starts a listner and handles 
    every client connection in a new thread.
    
    :param host: server's host, defaults to '127.0.0.1'
    :type host: str, optional
    :param port: server's port, defaults to 8000
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



def _save_binary(path, snapshot):
    """Saves binary blobs to a given path.
    
    :param path: filesystem path
    :type path: pathlib.Path
    :param snapshot: snapshot with blobs
    :type snapshot: Snapshot
    """
    if not path.exists():
        path.mkdir(parents=True)
    (path / 'color_image').write_bytes(snapshot.color_image.data)
    depth_image_data = np.array(snapshot.depth_image.data)
    np.save(str(path / 'depth_image'), depth_image_data)