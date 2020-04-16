import json

from colinthecomputer.utils import filtered_dict

def parse_pose(data):
    """Parse pose from snapshot data.
    
    :param data: snapshot as consumbed from the message queue
    :type data: json
    :returns: parsed snapshot pose 
    :rtype: json
    """
    data = json.loads(data)
    pose = filtered_dict(data, ['user_id', 'datetime'])
    print(data)
    pose['data'] = data['pose']
    print(json.dumps(pose))
    return json.dumps(pose)

parse_pose.field = 'pose'