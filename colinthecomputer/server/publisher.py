from colinthecomputer.mq_drivers import rabbitmq_driver
from colinthecomputer.protocol import ColorImage, DepthImage, Snapshot
from colinthecomputer.utils import make_path
import colinthecomputer.mq_drivers as drivers

from google.protobuf.json_format import MessageToDict
import json
import pathlib
import numpy as np
from furl import furl

# todo env variable
directory = pathlib.Path('/home/user/colinfs/raw_data') # TODO


def produce_publisher(mq_url):
    """Produce a publish function for the server,
    which receives a message and publishes it to the message queue.
    
    :param mq_url: a url describing the mq, in the form 'mq://host:port'
    :type mq_url: str
    :returns: a publish function
    :rtype: function
    """
    mq_url = furl(mq_url)
    mq, host, port = mq_url.scheme, mq_url.host, mq_url.port
    driver = drivers[mq]
    
    def publish(message):
        """Publish message to the message queue.

        The message is given as the protocol User, Snapshot
        and is converted to json before publishing.
        BLOBS are stored in the fs, with only their path being uploaded to the mq.
        
        :param message: message to be published
        :type message: (User, Snapshot)
        """
        user, snapshot = message
        user_id = user.user_id
        message = user_message(user)
        driver.publish(message, host, port, segment='results', topic='user')

        # Save BLOBs to filesystem
        datetime = snapshot.datetime_object().strftime('%Y-%m-%d_%H-%M-%S-%f')
        path = directory / str(user_id) / datetime
        if not path.exists():
            path.mkdir()
        (path / 'color_image').write_bytes(snapshot.color_image.data)
        depth_image_data = np.array(snapshot.depth_image.data)
        np.save(str(path / 'depth_image'), depth_image_data)

        # Create JSON representation of snapshot without BLOBs
        message = snapshot_message(snapshot, user_id, path)
        driver.publish(message, host, port, segment='raw_data')
        print('published :)')
   
    return publish


def user_message(user):
    """Convert protocol-user to json.

    :param user: user object
    :type user: User
    :returns: user information json
    :rtype: json
    """
    user_id = user.user_id
    user_dict = MessageToDict(user)
    user_dict['user_id'] = int(user_dict.pop('userId'))
    user_dict['gender'] = user.get_gender_char()
    print(user_dict)
    return json.dumps(user_dict)

def snapshot_message(snapshot, user_id, image_path):
    """Convert protocol-snapshot to json, replacing binary data with path to data.

    :param snapshot: snapshot object
    :type snapshot: Snapshot
    :param user_id: user id corresponding the snapshot
    :type user_id: int
    :param image_path: path to BLOBS
    :type image_path: str
    :returns: snapshot information json
    :rtype: json
    """
    snapshot_metadata = Snapshot()
    snapshot_metadata.CopyFrom(snapshot)
    snapshot_metadata.color_image.ClearField('data')
    snapshot_metadata.depth_image.ClearField('data')
    snapshot_dict = MessageToDict(snapshot_metadata, including_default_value_fields=True)
    snapshot_dict['user_id'] = user_id
    snapshot_dict['color_image']['path'] = str(image_path / 'color_image')
    snapshot_dict['depth_image']['path'] = str(image_path / 'depth_image.npy')
    print(snapshot_dict)
    return json.dumps(snapshot_dict)