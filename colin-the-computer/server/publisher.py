from ..mq_drivers import rabbitmq_driver
from ..protocol import ColorImage, DepthImage, Snapshot

from google.protobuf.json_format import MessageToJson
import json
import pathlib
from furl import furl


drivers = {'rabbitmq':rabbitmq_driver}
directory = pathlib.Path('/home/user/test/raw_data/') # TODO


def produce_publisher(mq_url):
    mq_url = furl(mq_url)
    mq, host, port = mq_url.scheme, mq_url.host, mq_url.port
    driver = drivers[mq]
    
    def publish(snapshot):
        # Create JSON representation of snapshot without BLOBs
        snapshot_metadata = Snapshot()
        snapshot_metadata.CopyFrom(snapshot)
        snapshot_metadata.color_image.ClearField('data')
        snapshot_metadata.depth_image.ClearField('data')
        # TODO: encode path
        json_snapshot = MessageToJson(snapshot_metadata)
        message = bytes(json.dumps(json_snapshot), 'utf-8')
        driver.broadcast_publish(message, host, port, segment='raw_data')

        # TODO: figure out to where the publisher publishes
        # Save BLOBs to filesystem
        datetime = snapshot.datetime_object().strftime('%Y-%m-%d_%H-%M-%S-%f')
        path = directory / '42'
        if not path.exists():
            path.mkdir()
        path /= datetime
        if not path.exists():
            path.mkdir()

        (path / 'color_image').write_bytes(snapshot.color_image.data)
        # TODO: how do i save the depth image?
        (path / 'depth_image').write_bytes(snapshot.depth_image.SerializeToString())    
    return publish
