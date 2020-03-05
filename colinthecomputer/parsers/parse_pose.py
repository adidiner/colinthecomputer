import json

def parse_pose(data):
    data = json.loads(data) # TODO: wtf
    pose = {}
    pose['data'] = data['pose']
    pose['user_id'], pose['datetime'] = data['userId'], data['datetime']
    return json.dumps(pose)

parse_pose.field = 'pose'