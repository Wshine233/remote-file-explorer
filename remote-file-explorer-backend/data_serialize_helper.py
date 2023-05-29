import json
from pathlib import Path
from typing import Union
import file_helper as fh


def format_mounts(mounts):
    """对挂载列表数据进行格式化

    对数据进行校验并尝试修正, 将数据类型转换为用于序列化的类型
    """

    result = []
    for mount in mounts.values():
        result.append({
            'target': str(Path(mount['target']).resolve()),
            'root': str(Path(mount['root']))
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

    raw = json.dumps(format_mounts(mounts))
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


def deserialize_mounts(raw, load_path: Union[str, None]=None):
    """对挂载列表数据进行反序列化

    对数据进行校验并尝试修正, 将数据类型转换为用于使用的类型
    """

    if load_path is not None and Path(load_path).exists():
        with open(load_path, 'r') as f:
            raw = f.read()
    return object_mounts(json.loads(raw))


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

