
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
    return {snapshot_id: result_name}