import pathlib
import threading

from .utils import Listener
from .utils import parsers
from .protocol import Hello
from .protocol import Config
from .protocol import Snapshot


HEADER_SIZE = 20


class Context:
    def __init__(self, directory):
        self.directory = directory


class Handler(threading.Thread):
    lock = threading.Lock()

    def __init__(self, client, data_dir):
        super().__init__()
        self.client = client
        self.data_dir = data_dir

    def run(self):
        with self.client:
            # Receive hello
            data = self.client.receive_message()
            hello = Hello.deserialize(data)
            # Send config
            config = Config([field for field in parsers])
            data = config.serialize()
            self.client.send_message(data)
            # Receive snapshot
            data = self.client.receive_message()
            snapshot = Snapshot.deserialize(data)

        # TODO: figure out exception handling

        with Handler.lock:
            self.save_snapshot(hello, snapshot)

    def save_snapshot(self, hello, snapshot):
        datetime = snapshot.datetime.strftime('%Y-%m-%d_%H-%M-%S-%f')
        path = pathlib.Path(self.data_dir) / f'{hello.user_id}'
        if not path.exists():
            path.mkdir()
        path /= datetime
        if not path.exists():
            path.mkdir()
        context = Context(path)
        for parser in parsers.values():
            parser(context, snapshot)


def run_server(address, data_dir):
    host, port = address
    # Setup server
    with Listener(host=host, port=port) as server:
        while True:
            # Recieve message
            client = server.accept()
            handler = Handler(client, data_dir)
            handler.start()
