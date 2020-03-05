from colinthecomputer.mq_drivers import rabbitmq_driver
from colinthecomputer.protocol import ColorImage, DepthImage, Snapshot
from colinthecomputer.utils import make_path

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
        user, snapshot = message
        user_id = user.user_id
        message = user_message(user)
        driver.publish(message, host, port, segment='results', topic='user')

        # TODO: figure out to where the publisher publishes
        # Save BLOBs to filesystem
        datetime = snapshot.datetime_object().strftime('%Y-%m-%d_%H-%M-%S-%f')
        path = directory / str(user_id) / datetime
        if not path.exists():
            path.mkdir()
        (path / 'color_image').write_bytes(snapshot.color_image.data)
        # TODO: how do i save the depth image?
        depth_image_data = np.array(snapshot.depth_image.data)
        np.save(str(path / 'depth_image'), depth_image_data)

        # Create JSON representation of snapshot without BLOBs
        message = snapshot_message(snapshot, user_id, path)
        driver.publish(message, host, port, segment='raw_data')
        print('published :)')
   
    return publish


def user_message(user):
    user_id = user.user_id
    # TODO: does this make sense?
    user_dict = MessageToDict(user)
    user_dict['user_id'] = user_dict.pop('userId')
    user_dict['gender'] = user.get_gender_char()
    print(user_dict)
    return json.dumps(user_dict)

def snapshot_message(snapshot, user_id, image_path):
    snapshot_metadata = Snapshot()
    snapshot_metadata.CopyFrom(snapshot)
    snapshot_metadata.color_image.ClearField('data')
    snapshot_metadata.depth_image.ClearField('data')
    snapshot_dict = MessageToDict(snapshot_metadata)
    snapshot_dict['userId'] = user_id
    snapshot_dict['colorImage']['path'] = str(image_path / 'color_image')
    snapshot_dict['depthImage']['path'] = str(image_path / 'depth_image.npy')
    return json.dumps(snapshot_dict)