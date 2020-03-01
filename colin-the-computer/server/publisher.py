import pathlib

from . import queue_drivers
from ..protocol import ColorImage, DepthImage, Snapshot

from google.protobuf.json_format import MessageToJson


drivers = {'rabbitmq': queue_drivers.rabbitmq_driver}
mq = 'rabbitmq' # TODO
directory = pathlib.Path('/home/user/test/raw_data/') # TODO


def publish(snapshot):
    driver = drivers[mq]
    # Create JSON representation of snapshot without BLOBs
    snapshot_metadata = Snapshot()
    snapshot_metadata.CopyFrom(snapshot)
    snapshot_metadata.color_image.ClearField('data')
    snapshot_metadata.depth_image.ClearField('data')
    json_snapshot = MessageToJson(snapshot_metadata)
    #driver.publish(json_snapshot)
    print(json_snapshot)

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


