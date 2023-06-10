import json
from pathlib import Path
from typing import Union
import file_helper as fh


"""通用序列化方法"""
def serialize(data, save_path: Union[str, None]=None):
    """对数据进行序列化，请使用格式化后的数据
    """

    raw = json.dumps(data)
    if save_path is not None:
        path = Path(save_path)
        old_path = Path(save_path + '.old')
        if path.exists():
            path.rename(old_path)
        if not path.parent.exists():
            fh.create_folder(path.parent)
        with open(save_path, 'x') as f:
            f.write(raw)
        if old_path.exists():
            old_path.unlink()
    return raw


def deserialize(raw, load_path: Union[str, None]=None, default=None):
    """对数据进行反序列化，请自行处理格式化后的数据
    """

    if load_path is not None:
        if not Path(load_path).exists():
            return default
        with open(load_path, 'r') as f:
            raw = f.read()
    return json.loads(raw)



"""挂载列表"""
def format_mounts(mounts):
    """对挂载列表数据进行格式化

    对数据进行校验并尝试修正, 将数据类型转换为用于序列化的类型
    """

    result = []
    for mount in mounts.values():
        result.append({
            'target': str(Path(mount['target']).resolve()).replace('\\', '/'),
            'root': str(Path(mount['root'])).replace('\\', '/')
        })
    return result


def object_mounts(mounts):
    """对挂载列表数据进行对象化

    对数据进行校验并尝试修正, 将数据类型转换为用于使用的类型
    """

    result = {}
    for mount in mounts:
        key = mount['target']
        result[Path(key).resolve()] = mount
    return result


def serialize_mounts(mounts, save_path: Union[str, None]=None):
    """对挂载列表数据进行序列化

    对数据进行校验并尝试修正, 将数据类型转换为用于序列化的类型
    """

    return serialize(format_mounts(mounts), save_path)


def deserialize_mounts(raw, load_path: Union[str, None]=None, defaultValue={}):
    """对挂载列表数据进行反序列化

    对数据进行校验并尝试修正, 将数据类型转换为用于使用的类型
    """

    return object_mounts(deserialize(raw, load_path, defaultValue))


"""文件权限表"""
def format_perms(perms):
    """对文件权限表数据进行格式化

    对数据进行校验并尝试修正, 将数据类型转换为用于序列化的类型
    """

    result = []
    for perm in perms.values():
        result.append({
            'file': str(Path(perm['file']).resolve()).replace('\\', '/'),
            'visibleGroup': perm['visibleGroup'],
            'visibleUser': perm['visibleUser'],
            'invisibleUser': perm['invisibleUser'],
            'rules': perm['rules']
        })
    return result


def object_perms(perms):
    """对文件权限表数据进行对象化

    对数据进行校验并尝试修正, 将数据类型转换为用于使用的类型
    """

    result = {}
    for perm in perms:
        key = perm['file']
        result[Path(key).resolve()] = perm
    return result


def serialize_perms(raw, save_path: Union[str, None]=None):
    """对文件权限表数据进行序列化

    对数据进行校验并尝试修正, 将数据类型转换为用于序列化的类型
    """

    return serialize(format_perms(raw), save_path)


def deserialize_perms(raw, load_path: Union[str, None]=None, defaultValue={}):
    """对文件权限表数据进行反序列化

    对数据进行校验并尝试修正, 将数据类型转换为用于使用的类型
    """

    return object_perms(deserialize(raw, load_path, defaultValue))


"""忽略文件表"""
def format_ignores(ignores):
    """对忽略文件表数据进行格式化

    对数据进行校验并尝试修正, 将数据类型转换为用于序列化的类型
    """

    result = []
    for ignore in ignores:
        result.append(str(Path(ignore).resolve()).replace('\\', '/'))
    return result

def object_ignores(ignores):
    """对忽略文件表数据进行对象化

    对数据进行校验并尝试修正, 将数据类型转换为用于使用的类型
    """

    result = []
    for ignore in ignores:
        result.append(Path(ignore).resolve())
    return result

def serialize_ignores(raw, save_path: Union[str, None]=None):
    """对忽略文件表数据进行序列化

    对数据进行校验并尝试修正, 将数据类型转换为用于序列化的类型
    """

    return serialize(format_ignores(raw), save_path)

def deserialize_ignores(raw, load_path: Union[str, None]=None, defaultValue={}):
    """对忽略文件表数据进行反序列化

    对数据进行校验并尝试修正, 将数据类型转换为用于使用的类型
    """

    return object_ignores(deserialize(raw, load_path, defaultValue))


"""用户表"""
def format_users(users):
    return users

def object_users(users):
    return users

def serialize_users(raw, save_path: Union[str, None]=None):
    return serialize(format_users(raw), save_path)

def deserialize_users(raw, load_path: Union[str, None]=None, defaultValue=[]):
    return object_users(deserialize(raw, load_path, defaultValue))


"""会话表"""
def format_sessions(sessions):
    return sessions

def object_sessions(sessions):
    return sessions

def serialize_sessions(raw, save_path: Union[str, None]=None):
    return serialize(format_sessions(raw), save_path)

def deserialize_sessions(raw, load_path: Union[str, None]=None, defaultValue=[]):
    return object_sessions(deserialize(raw, load_path, defaultValue))


"""权限组表"""
def format_groups(groups):
    return groups

def object_groups(groups):
    return groups

def serialize_groups(raw, save_path: Union[str, None]=None):
    return serialize(format_groups(raw), save_path)

def deserialize_groups(raw, load_path: Union[str, None]=None, defaultValue=[]):
    return object_groups(deserialize(raw, load_path, defaultValue))


"""分享表"""
def format_shares(shares):
    return shares

def object_shares(shares):
    return shares

def serialize_shares(raw, save_path: Union[str, None]=None):
    return serialize(format_shares(raw), save_path)

def deserialize_shares(raw, load_path: Union[str, None]=None, defaultValue=[]):
    return object_shares(deserialize(raw, load_path, defaultValue))




    


if __name__ == '__main__':
    import config as cfg

    mounts = {
        Path('D:/[]临时工作间'): {
            'target': 'D:/[]临时工作间',   # 被挂载的目录/文件位置，必须是绝对路径且唯一；启动时会检查是否存在；
            'root': '/临时工作间',   # 挂载到的路径，必须以/开头，且唯一；一个挂载点只能挂载一个目录/文件; 不能直接挂载到'/'
        },
        Path('D:/[]临时工作间/TEST2'): {
            'target': 'D:/[]临时工作间/TEST2',
            'root': '/TEST',
        }
    }

    serialize_mounts(mounts, cfg.mount_data_path)
    mounts = deserialize_mounts(None, cfg.mount_data_path)
    print(mounts)

