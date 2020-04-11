import json

def parse_feelings(data):
    data = json.loads(data)
    feelings = {}
    feelings['data'] = {'feelings': data['feelings']}
    feelings['user_id'], feelings['datetime'] = data['user_id'], data['datetime']
    print(feelings)
    return json.dumps(feelings)

parse_feelings.field = 'feelings'