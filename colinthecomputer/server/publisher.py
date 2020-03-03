from colinthecomputer.mq_drivers import rabbitmq_driver
from colinthecomputer.protocol import ColorImage, DepthImage, Snapshot

from google.protobuf.json_format import MessageToDict
import json
import pathlib
import numpy as np
from furl import furl


drivers = {'rabbitmq':rabbitmq_driver}
directory = pathlib.Path('/home/user/colinfs/raw_data') # TODO


def produce_publisher(mq_url):
    mq_url = furl(mq_url)
    mq, host, port = mq_url.scheme, mq_url.host, mq_url.port
    driver = drivers[mq]
    
    def publish(message):
        user_id, snapshot = message
        # TODO: figure out to where the publisher publishes
        # Save BLOBs to filesystem
        datetime = snapshot.datetime_object().strftime('%Y-%m-%d_%H-%M-%S-%f')
        path = directory / str(user_id)
        if not path.exists():
            path.mkdir()
        path /= datetime
        if not path.exists():
            path.mkdir()

        (path / 'color_image').write_bytes(snapshot.color_image.data)
        # TODO: how do i save the depth image?
        depth_image_data = np.array(snapshot.depth_image.data)
        np.save(str(path / 'depth_image'), depth_image_data)

        # Create JSON representation of snapshot without BLOBs
        snapshot_metadata = Snapshot()
        snapshot_metadata.CopyFrom(snapshot)
        snapshot_metadata.color_image.ClearField('data')
        snapshot_metadata.depth_image.ClearField('data')
        snapshot_dict = MessageToDict(snapshot_metadata)
        snapshot_dict['userID'] = user_id
        snapshot_dict['colorImage']['path'] = str(path / 'color_image')
        snapshot_dict['depthImage']['path'] = str(path / 'depth_image')
        message = bytes(json.dumps(snapshot_dict), 'utf-8')
        driver.publish(message, host, port, segment='raw_data')
        print(snapshot_dict)
        print('published :)')
   
    return publish
