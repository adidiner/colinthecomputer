tmpdir = None

def init_db(name, host, port, username, password):
    return

def get_users():
    return 'users'

def get_user_info(user_id):
    return {user_id: 'user_info'}

def get_snapshots(user_id):
    return {user_id: 'snapshots'}

def get_snapshot_info(snapshot_id):
    return {snapshot_id: 'snapshot_info'}

def get_result(snapshot_id, result_name):
    if result_name not in ['pose', 'color_image', 'depth_image', 'feelings']:
        return
    if result_name in ['color_image', 'depth_image']:
        return {'path': f'{tmpdir}/{result_name}.jpg'}
    return {'result': result_name}

getters = {'users': get_users, 'user_info': get_user_info,
           'snapshots': get_snapshots, 'snapshot_info': get_snapshot_info,
           'result': get_result}