import json

def parse_feelings(data):
    data = json.loads(data)
    feelings['data'] = data['feelings']
    feelings['userID'], feelings['datetime'] = data['userID'], feelings['datetime']
    return json.dumps(feelings)

parse_feelings.field = 'feelings'