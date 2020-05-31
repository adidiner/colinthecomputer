import json

from colinthecomputer.utils import filtered_dict

count = 1

def parse_pose(data):
    """
    Parse pose from snapshot data.

    :param data: snapshot as consumbed from the message queue
    :type data: json
    :returns: parsed snapshot pose
    :rtype: json
    """
    data = json.loads(data)
    pose = filtered_dict(data, ['user_id', 'datetime'])
    pose['data'] = data['pose']
    global count
    count += 1
    if (count in {50, 100, 200, 300, 350, 360, 365, 367}):
        print(count)
    return json.dumps(pose)


parse_pose.field = 'pose'
