import pathlib as pl
from pathlib import Path
import shutil


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
    if not path.exists():
        return False
    if path.is_dir():
        path.rmdir()
    else:
        path.unlink()
    return True


def rename_file(path: Path, name: str):
    if not path.exists():
        return False
    new_path = path.parent / name
    if new_path.exists():
        return False
    path.rename(new_path)
    return True


def move_file(path: Path, new_path: Path):
    if not path.exists():
        return False
    if new_path.exists():
        return False
    if not new_path.parent.exists():
        create_folder(new_path.parent)
    shutil.move(str(path), str(new_path))
    return True


def copy_file(path: Path, new_path: Path):
    if not path.exists():
        return False
    if new_path.exists():
        return False
    if not new_path.parent.exists():
        create_folder(new_path.parent)
    shutil.copy(str(path), str(new_path))
    return True


def same_path(path1: Path, path2: Path):
    return path1.resolve() == path2.resolve()