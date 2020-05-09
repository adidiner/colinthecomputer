import colinthecomputer.protocol as ptc
from colinthecomputer.utils import make_path
import colinthecomputer.mq_drivers as drivers

from google.protobuf.json_format import MessageToDict
import json
import pathlib
import numpy as np
from furl import furl


class Publisher:
    """Publisher which publishes messages to a given message queue.
    
    :param mq_url: a url describing the mq, in the form 'mq://host:port'
    :type mq_url: str
    """
    def __init__(self, mq_url, directory):
        mq_url = furl(mq_url)
        mq, self.host, self.port, self.mq_url = mq_url.scheme, mq_url.host, mq_url.port, mq_url
        self.driver = drivers[mq]
        self.directory = pathlib.Path(directory)

    def __repr__(self):
        return f'Publisher(mq_url={self.mq_url}, blob_dir={self.directory})'

    def publish(self, message):
        """Publish message to the message queue.

        The message is given as the protocol User, Snapshot
        and is converted to json before publishing.
        BLOBS are stored in the fs, with only their path being uploaded to the mq.
        
        :param message: message to be published
        :type message: (User, Snapshot)
        """
        user, snapshot = message
        self.driver.share_publish(_json_user_message(user),
                                  self.host,
                                  self.port,
                                  topic='user',
                                  segment='results')

        # Save BLOBs to filesystem
        path = self.directory / str(user.user_id) / str(snapshot.datetime)
        _save_binary(path, snapshot)

        # Create JSON representation of snapshot without BLOBs
        self.driver.task_publish(_json_snapshot_message(snapshot, user.user_id, path),
                                 self.host, 
                                 self.port, 
                                 segment='raw_data')


def _json_user_message(user):
    """Convert protocol-user to json.

    :param user: user object
    :type user: User
    :returns: user information json
    :rtype: json
    """
    user_id = user.user_id
    user_dict = MessageToDict(user,
                              preserving_proto_field_name=True)
    print(user_dict)
    user_dict['gender'] = ptc.gender_enum_to_char(user.gender)
    return json.dumps(user_dict)


def _json_snapshot_message(snapshot, user_id, image_path):
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
    snapshot_metadata = ptc.Snapshot()
    snapshot_metadata.CopyFrom(snapshot)
    snapshot_metadata.color_image.ClearField('data')
    snapshot_metadata.depth_image.ClearField('data')
    snapshot_dict = MessageToDict(snapshot_metadata, 
                                  preserving_proto_field_name=True, 
                                  including_default_value_fields=True)
    snapshot_dict['user_id'] = user_id
    snapshot_dict['color_image']['data'] = str(image_path / 'color_image')
    snapshot_dict['depth_image']['data'] = str(image_path / 'depth_image.npy')
    return json.dumps(snapshot_dict)


def _save_binary(path, snapshot):
    if not path.exists():
        path.mkdir(parents=True)
    (path / 'color_image').write_bytes(snapshot.color_image.data)
    depth_image_data = np.array(snapshot.depth_image.data)
    np.save(str(path / 'depth_image'), depth_image_data)