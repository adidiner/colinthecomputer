import json

def parse_pose(data):
    data = json.loads(data) # TODO: wtf
    pose = data['pose']
    pose['userID'] = data['userID']
    return json.dumps(pose)

parse_pose.field = 'pose'