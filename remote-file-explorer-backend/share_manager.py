import config as cfg
import crypto
import file_manager as fm
import data_serialize_helper as dsh
from pathlib import Path
import os


shares = [
    {
        'id': 'share_sample',
        'user_id': 'admin',
        'path_list': ['/Example Folder/Example File.txt',
                      '/Example Folder/Example Folder 2/Example File 2.txt',
                      '/Share Folder'],
        'password': '1234',
        'create_time': 1035421256,
        'expired': 1235421256   # 过期时间戳
    }
]


def load_data():
    global shares
    shares = dsh.deserialize_shares(None, cfg.share_data_path)


def save_data():
    dsh.serialize_shares(shares, cfg.share_data_path)


def add_share(user_id, path_list, password, expired):
    share_id = crypto.uuid_v4()
    share = {
        'id': share_id,
        'user_id': user_id,
        'path_list': path_list,
        'password': password,
        'create_time': crypto.time(),
        'expired': expired
    }
    shares.append(share)
    save_data()
    return share_id


def delete_share(share_id):
    for share in shares:
        if share['id'] == share_id:
            shares.remove(share)
            save_data()
            return True
    return False


def get_share_by_id(share_id):
    for share in shares:
        if share['id'] == share_id:
            return share
    return None


def get_share_by_user(user_id):
    result = []
    for share in shares:
        if share['user_id'] == user_id:
            result.append(share)
    return result


def verify_password(share_id, password):
    share = get_share_by_id(share_id)
    if share is None:
        return False
    return share['password'] == password


def list_root_file(share_id):
    share = get_share_by_id(share_id)
    if share is None:
        return None
    result = []
    for path in share['path_list']:
        type = fm.get_file_type(path)
        result.append({
            'name': path.split('/')[-1],
            'path': path,
            'type': type,
            'size': None if type == 0 else fm.get_file_size(path),
            'time_modified': fm.get_file_time_modified(path),
        })
    return result


def list_file(share_id, path: str):
    path = path.strip()
    if path == '/':
        return list_root_file(share_id)

    real_path = fm.get_file_real_path(path)
    if real_path is None or not real_path.is_dir():
        return None
    
    files = os.listdir(str(real_path))
    files = [real_path / file for file in files]

    result = []
    for file in files:
        type = 0 if file.is_dir() else 1
        result.append({
            'name': file.name,
            'path': path + '/' + file.name,
            'type': type,
            'size': None if type == 0 else file.stat().st_size,
            'time_modified': file.stat().st_mtime,
        })
    return result



