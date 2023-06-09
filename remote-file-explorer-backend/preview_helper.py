import crypto
import file_manager as fm


def get_preview_file(token, user_id, ip):
    data = crypto.preview_token_decrypt(token, user_id)
    if data is None:
        return None
    
    if user_id != data['user_id'] or ip != data['ip']:
        return None
    
    if data['expire_time'] < crypto.time():
        return None
    
    path = data['path']
    real_path = fm.get_file_real_path(path)
    if real_path is None or real_path.is_dir():
        return None
    
    return str(real_path)