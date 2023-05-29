from datetime import datetime
import pathlib
import hashlib
import uuid


def md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def sha256(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def uuid_v4():
    return str(uuid.uuid4())


def time():
    return int(datetime.now().timestamp()*1000)