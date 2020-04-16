import json

from colinthecomputer.utils import filtered_dict


def parse_feelings(data):
    """Parse feelings from snapshot data.
    
    :param data: snapshot as consumbed from the message queue
    :type data: json
    :returns: parsed snapshot feelings 
    :rtype: json
    """
    data = json.loads(data)
    feelings = filtered_dict(data, ['user_id', 'datetime'])
    feelings['data'] = data['feelings']
    print(feelings)
    return json.dumps(feelings)

parse_feelings.field = 'feelings'