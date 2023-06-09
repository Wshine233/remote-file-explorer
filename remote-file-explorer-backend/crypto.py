from datetime import datetime
import pathlib
import hashlib
from cryptography.fernet import Fernet
import json
import uuid
import base64
import config as cfg


def md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def uuid_v4():
    return str(uuid.uuid4())


def time():
    return int(datetime.now().timestamp()*1000)


def base64_encode(text):
    return base64.b64encode(text.encode('utf-8'))


def encrypt(text, key):
    try:
        f = Fernet(key)
        return f.encrypt(text.encode('utf-8')).decode('utf-8')
    except:
        return None


def decrypt(text, key):
    try:
        f = Fernet(key)
        return f.decrypt(text.encode('utf-8')).decode('utf-8')
    except:
        return None


def preview_token(user_id, path, ip):
    # 可逆向解密的token
    expire_time = time() + cfg.preview_expire_time
    data = {
        'user_id': user_id,
        'path': path,
        'expire_time': expire_time,
        'ip': ip
    }
    key = base64_encode(md5(user_id))
    
    return encrypt(json.dumps(data), key)


def preview_token_decrypt(token, user_id):
    # 解密token
    key = base64_encode(md5(user_id))
    raw = decrypt(token, key)
    return json.loads(raw) if raw else None


if __name__ == '__main__':
    print(Fernet.generate_key())
    
    token = preview_token('Wshine', '/a/b', '127.0.0.1:3000')
    print(token)
    print(preview_token_decrypt(token, 'Wshine'))
