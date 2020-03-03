import json

def parse_feelings(data):
    data = json.loads(data)
    feelings = data['feelings']
    feelings['userID'] = data['userID']
    return json.dumps(feelings)

parse_feelings.field = 'feelings'