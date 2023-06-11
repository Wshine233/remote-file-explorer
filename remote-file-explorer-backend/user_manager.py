import pathlib
import random
import crypto
import config as cfg
import data_serialize_helper as dsh
import permission_manager as pm


users = [
    {
        'name': 'Administrator',
        'id': 'admin',
        'passwordHash': '96cae35ce8a9b0244178bf28e4966c2ce1b8385723a96a6b838858cdd6ca0a1e',  # 123123
        'permissionGroup': 'super',
        'permission': "*****",
        'joinTime': 0
    }
]


sessions = [
    {
        'id': 'session_sample',
        'expired': 0,
        'user': 'admin'
    }
]



def load_data():
    global users, sessions
    users = dsh.deserialize_users(None, cfg.user_data_path)
    sessions = dsh.deserialize_sessions(None, cfg.session_data_path)


def save_data():
    dsh.serialize_users(users, cfg.user_data_path)
    dsh.serialize_sessions(sessions, cfg.session_data_path)


def get_user_by_id(user_id):
    for user in users:
        if user['id'] == user_id:
            return user
    return None


def get_user_id(session_id, check_expired=True):
    for session in sessions:
        if session['id'] == session_id:
            if check_expired and session['expired'] < crypto.time():
                return None
            return session['user']
    return None


def get_user_by_session(session_id, check_expired=True):
    user_id = get_user_id(session_id, check_expired)
    if user_id is None:
        return None
    return get_user_by_id(user_id)


def get_user_permission(user_id):
    user = get_user_by_id(user_id)
    if user is None:
        return None
    return user['permission']


def add_user(id, password_hash, name, permission_group, permission):
    if get_user_by_id(id) is not None:
        return False

    users.append({
        'name': name,
        'id': id,
        'passwordHash': password_hash,
        'permissionGroup': permission_group,
        'permission': permission,
        'joinTime': crypto.time(),
    })

    save_data()
    return True


def remove_user(id):
    for user in users:
        if user['id'] == id:
            users.remove(user)
            save_data()
            return True
    return False


def update_user(user_id, keys: list, values: list):
    user = get_user_by_id(user_id)
    if user is None:
        return False
    for i in range(len(keys)):
        if keys[i] == 'passwordHash':
            continue
        if keys[i] == 'permission':
            if not pm.validate_permission(values[i]):
                values[i] = user.get('permission', '*****')
        user[keys[i]] = values[i]
    
    save_data()
    return True


def update_password(user_id, old_password_hash, new_password_hash):
    user = get_user_by_id(user_id)
    if user is None:
        return False
    if user['passwordHash'] != old_password_hash:
        return False
    user['passwordHash'] = new_password_hash

    save_data()
    return True


def get_user_info(user_id, keys: list):
    user = get_user_by_id(user_id)
    if user is None:
        return {}
    result = {}
    for key in keys:
        if key not in user or key == 'passwordHash':
            continue
        if key == 'permissionGroup' and pm.get_group(user[key]) is None:
            result[key] = pm.get_default_group()
            continue
        result[key] = user[key]
    return result


def login(user_id, password_hash):
    user = get_user_by_id(user_id)
    if user is None:
        return None
    if user['passwordHash'] != password_hash:
        return None
    return create_session(user_id)


def logout(session_id):
    for session in sessions:
        if session['id'] == session_id:
            sessions.remove(session)
            return True
    return False


def clear_expired_session():
    for session in sessions[:]:
        if session['expired'] < crypto.time():
            sessions.remove(session)
    save_data()


def get_session(session_id):
    for session in sessions:
        if session['id'] == session_id:
            return session
    return None


def create_session(user_id):
    clear_expired_session()
    session_id = crypto.uuid_v4()
    sessions.append({
        'id': session_id,
        'expired': crypto.time() + cfg.session_expire_time,
        'user': user_id
    })
    save_data()
    return session_id


def delete_session(session_id):
    session = get_session(session_id)
    if session is None:
        return False
    sessions.remove(session)
    save_data()
    return True


def verify_session(session_id):
    session = get_session(session_id)
    if session is None:
        return False
    if session['expired'] < crypto.time():
        return False
    return True


def update_session(session_id):
    session = get_session(session_id)
    if session is None:
        return None
    if session['expired'] < crypto.time():
        return None
    session['id'] = crypto.uuid_v4()
    session['expired'] = crypto.time() + cfg.session_expire_time

    save_data()
    return session['id']


def session_login(session_id):
    return update_session(session_id)


def list_users(keys):
    result = []
    for user in users:
        result.append(get_user_info(user['id'], keys))
    return result



load_data()