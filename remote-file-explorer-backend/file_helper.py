import pathlib as pl
from pathlib import Path
import shutil
import send2trash


def get_file_name(path: Path):
    return path.name


def get_file_size(path: Path):
    return path.stat().st_size


def get_file_type(path: Path):
    if path.is_dir():
        return 'dir'
    elif path.is_file():
        return 'file'
    else:
        return 'unknown'


def get_file_last_modified(path: Path):
    return path.stat().st_mtime


def get_file_last_accessed(path: Path):
    return path.stat().st_atime


def get_file_created(path: Path):
    return path.stat().st_ctime


# Attribute指令列表
ATTRIBUTES = {
    'file_name': get_file_name,
    'file_size': get_file_size,
    'file_type': get_file_type,
    'file_last_modified': get_file_last_modified,
    'file_last_accessed': get_file_last_accessed,
    'file_created': get_file_created
}


def get_file_attribute(path: Path, attribute: str):
    if attribute not in ATTRIBUTES:
        return None

    return ATTRIBUTES[attribute](path)


def register_attribute(name: str, getter):
    """注册新的文件attribute

    Args:
        name (str): attribute名称
        getter (function): 值获取器, 格式: getter(path)

    Returns:
        _bool_: _是否注册成功, False则代表名称已存在, 无法注册_
    """
    if name in ATTRIBUTES:
        return False
    ATTRIBUTES[name] = getter
    return True


def create_folder(path: Path):
    if path.exists():
        return False
    path.mkdir(parents=True, exist_ok=True)
    return True


def delete_file(path: Path):
    """将文件移动到回收站"""
    if not path.exists():
        return False
    if path.is_dir():
        send2trash.send2trash(str(path))
    else:
        send2trash.send2trash(str(path))
    return True


def validate_file_name(name: str):
    if name == '':
        return False
    invalid_chars = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']
    for char in invalid_chars:
        if char in name:
            return False
    return True


def rename_file(path: Path, name: str):
    if not validate_file_name(name):
        return False
    if not path.exists():
        return False
    new_path = path.parent / name
    if new_path.exists():
        return False
    path.rename(new_path)
    return True


def move_file(path: Path, new_path: Path):
    try:
        if not path.exists():
            return False, True, 'File not found.'
        if new_path.exists():
            return False, False, 'Target path already have a file with the same name.'
        if not new_path.parent.exists():
            create_folder(new_path.parent)
        shutil.move(str(path), str(new_path))
        return True, True, 'Move successfully.'  # 移动成功，由于是移动，原文件已经不存在，可以删除
    except Exception as e:
        return False, False, str(e)   # 未知原因移动失败，可重试，不能删除


def copy_file(path: Path, new_path: Path):
    try:
        if not path.exists():
            return False, True, 'File not found.'  # 文件不存在，该任务已经没有作用，可以删除
        if new_path.exists():
            return False, False, 'Target path already have a file with the same name.'  # 目标目录下存在同名文件，可以重命名后再复制，所以不能删除
        if not new_path.parent.exists():
            create_folder(new_path.parent)
        if path.is_dir():
            shutil.copytree(str(path), str(new_path))
        else:
            shutil.copyfile(str(path), str(new_path))
        return True, False, 'Copy successfully.'  # 复制成功，由于可以反复复制，所以不能删除
    except Exception as e:
        return False, False, str(e)  # 未知原因复制失败，可重试，不能删除


def check_copy_move(path: Path, new_path: Path):
    if not path.exists():
        return False, True, 'File not found.'  # 文件不存在，该任务已经没有作用，可以删除
    if new_path.exists():
        return False, False, 'Target path already have a file with the same name.'  # 目标目录下存在同名文件，可以重命名后再复制，所以不能删除
    return True, False, 'Valid.'  # 任务有效，不能删除


def same_path(path1: Path, path2: Path):
    return path1.resolve() == path2.resolve()


def to_path_str(path: Path):
    return str(path).replace('\\', '/')