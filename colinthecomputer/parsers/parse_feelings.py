import json

def parse_feelings(data):
    data = json.loads(data)
    feelings = {}
    feelings['data'] = data['feelings']
    feelings['user_id'], feelings['datetime'] = data['userId'], data['datetime']
    return json.dumps(feelings)

parse_feelings.field = 'feelings'