import json

def parse_pose(data):
    data = json.loads(data) # TODO: wtf
    pose['data'] = data['pose']
    pose['userID'], pose['datetime'] = data['userID'], data['datetime']
    return json.dumps(pose)

parse_pose.field = 'pose'