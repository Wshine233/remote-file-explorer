import permission_manager as pm
import user_manager as um
from pathlib import Path
import os
import config as cfg
import file_helper as fh
import data_serialize_helper as dsh


# 挂载列表
mounts = {
    Path('D:/[]临时工作间'): {
        'target': 'D:/[]临时工作间',   # 被挂载的目录/文件位置，必须是绝对路径且唯一；启动时会检查是否存在；
        'root': '/临时工作间',   # 挂载到的路径，必须以/开头，且唯一；一个挂载点只能挂载一个目录/文件; 不能直接挂载到'/'
    },
    Path('D:/_Pictures/【图片】'): {
        'target': 'D:/_Pictures/【图片】',
        'root': '/我的图片',
    }
}

# 文件权限列表
perms = {
    Path('D:/[]临时工作间'): {
        'file': 'D:/[]临时工作间',   # 目标目录/文件的绝对路径
        'visibleGroup': ['admin', 'restrict'],   # 可见的权限组
        'visibleUser': ['admin'],   # 可见的用户，覆盖权限组规则
        'invisibleUser': ['user1'],   # 不可见的用户，覆盖权限组规则
        'rules': [
            {
                'type': 0,   # 0为权限组规则，1为用户规则
                'target': 'admin',   # 目标权限组/用户
                'permission': '**-**',   # 权限
            },
            {
                'type': 0,
                'target': 'restrict',
                'permission': '-----'
            }
        ]
    },
    Path('D:/_Pictures/【图片】'): {
        'file': 'D:/_Pictures/【图片】',
        'visibleGroup': ['admin', 'restrict'],
        'visibleUser': ['admin'],
        'invisibleUser': ['user1'],
        'rules': [
            {
                'type': 0,
                'target': 'admin',
                'permission': '**-**'
            },
            {
                'type': 0,
                'target': 'restrict',
                'permission': '-----'
            }
        ]
    }
}

# 忽略列表（使用绝对路径）
ignores = [
    Path('D:/test/ignore').resolve()
]


def get_file_real_path(path, check_exists=True):
    path = Path(path)
    for mount in mounts.values():
        root = Path(mount['root'])
        if fh.same_path(path, root):
            real = Path(mount['target'])
            return real.resolve() if not check_exists or real.exists() else None
        
        if path.is_relative_to(root):
            real = Path(mount['target']) / path.relative_to(mount['root'])
            return real.resolve() if not check_exists or real.exists() else None
    return None


def validate_mount(target: Path, root):
    # 检查该文件是否存在
    if not Path(target).exists():
        return False
    
    # 检查该文件是否已经被挂载
    if target.resolve() in mounts:
        return False
    
    # 检查挂载点是否为根目录
    if root == '/':
        return False
    
    # 检查挂载点是否可用
    real_path = get_file_real_path(root)
    if real_path is not None:
        return False
    
    return True


def add_mount(target: Path, root):
    if not validate_mount(target, root):
        return False

    mounts[target.resolve()] = {
        'target': str(target.resolve()),
        'root': root
    }

    if target in ignores:
        ignores.remove(target)

    return True


def remove_mount(target: Path):
    if target not in mounts:
        return False

    del mounts[target]

    return True


def get_mount_roots(path):
    # 获得挂载路径对应文件的所有根挂载点
    list = []
    path = Path(path)
    for mount in mounts.values():
        root = Path(mount['root'])
        if fh.same_path(path, root):
            list.append(mount)
            continue

        if path.is_relative_to(root):
            list.append(mount)
    return list


def get_mount_root(path):
    # 获得挂载路径对应文件的根挂载点（最根部）
    list = get_mount_roots(path)
    if len(list) == 0:
        return None
    list.sort(key=lambda x: len(Path(x['target']).parents))
    return list[0]


def get_mount_parent(path):
    # 获得挂载路径对应文件的父挂载点（最靠近文件的）
    list = get_mount_roots(path)
    if len(list) == 0:
        return None
    list.sort(key=lambda x: len(Path(x['target']).parents), reverse=True)
    return list[0]


def is_mounted(target: Path):
    # 检查指定路径是否被挂载（包含挂载目录的子目录和文件）
    for mount in mounts:
        if fh.same_path(target, mount):
            return True
        if target.is_relative_to(mount):
            return True
    return False


def user_visible(path, user_id):
    """用户是否能看到指定的文件"""
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False
    if real_path in ignores:
        return False
    
    user_perm = pm.get_user_permission(user_id)
    user_group = um.get_user_info(user_id, ['permissionGroup'])['permissionGroup']
    if user_perm is None:
        return False
    
    parents = [real_path] + list(real_path.parents)
    parents.reverse()
    root_mount = get_mount_root(path)
    root_mount = root_mount['target'] if root_mount is not None else None
    visible = False
    for parent in parents:
        # 从父目录根部开始检查权限
        if root_mount is None or not parent.is_relative_to(root_mount):
            continue
        if parent in perms:
            file_perm = perms[parent]
            group_test = user_group in file_perm['visibleGroup']
            user_test = user_id in file_perm['visibleUser']
            block_test = user_id in file_perm['invisibleUser']
            if not block_test and (group_test or user_test):
                # 父目录可以看见，继续检查子目录
                visible = True
                continue
            # 父目录不可见，直接返回
            return False
        # 父目录没有权限设置，继续检查子目录，默认不可见
    return visible


def get_file_permission(path, user_id):
    path = Path(path)
    real_path = get_file_real_path(path, check_exists=False)
    if real_path is None:
        return None

    user_info = um.get_user_info(user_id, ['permission', 'permissionGroup'])
    user_perm = user_info['permission']
    user_group = user_info['permissionGroup']
    group_perm = pm.get_group_permission(user_group)
    
    if not user_visible(path, user_id):
        return "-----"
    
    parents = [real_path] + list(real_path.parents)
    result = pm.merge_permission(group_perm, user_perm)
    for parent in parents:
        # 从文件路径开始向父级目录检查权限，直到找到权限设置为止
        if parent not in perms:
            continue
        file_perm = perms[parent]
        group_rule = group_perm
        user_rule = user_perm
        for rule in file_perm['rules']:
            if rule['type'] == 0 and rule['target'] == user_group:
                group_rule = rule['permission']
            if rule['type'] == 1 and rule['target'] == user_id:
                user_rule = rule['permission']
        
        result = pm.merge_permission(group_perm, group_rule)
        user_perm = pm.merge_permission(user_perm, user_rule)
        result = pm.merge_permission(result, user_perm)
        return result
    return result


def get_file_info(paths: list, keys: list, user_id: str):
    ls = []
    for path in paths:
        real_path = get_file_real_path(path)
        if real_path is None:
            return None
        
        info = {}
        for key in keys:
            if key == 'permission':
                info[key] = get_file_permission(path, user_id)
                continue
            v = fh.get_file_attribute(real_path, key)
            if v is not None:
                info[key] = v
        ls.append(info)
    return ls


def generate_default_permission(path):
    result = {
        'file': '',
        'visibleGroup': [],
        'visibleUser': [],
        'invisibleUser': [],
        'rules': []
    }
    
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return result
    result['file'] = str(real_path)
    
    mount_root = get_mount_root(path)
    if mount_root is None:
        # 文件未挂载或因为某些原因无法获得挂载点，生成空权限
        return result
    mount_target = Path(mount_root['target'])
    
    parents = [real_path] + list(real_path.parents)
    for parent in parents:
        if not parent.is_relative_to(mount_target):
            continue
        if parent not in perms:
            continue
        parent_perm = perms[parent]
        result['visibleGroup'] += parent_perm['visibleGroup']
        result['visibleUser'] += parent_perm['visibleUser']
        result['invisibleUser'] += parent_perm['invisibleUser']
        result['rules'] += parent_perm['rules']
        break

    return result


def update_rule(perm, rule):
    for r in perm['rules']:
        if r['type'] == rule['type'] and r['target'] == rule['target']:
            r['permission'] = rule['permission']
    perm['rules'].append(rule)


def remove_rule(perm, type, target):
    for r in perm['rules']:
        if r['type'] == type and r['target'] == target:
            perm['rules'].remove(r)


def get_permission(path, default=None):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return default
    if real_path not in perms:
        return default
    return perms[real_path]


def add_permission_rule(path, rule):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False
    
    perm = get_permission(path, generate_default_permission(path))
    update_rule(perm, rule)
    perms[real_path] = perm


def remove_permission_rule(path, type, target):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False
    
    perm = get_permission(path, generate_default_permission(path))
    remove_rule(perm, type, target)
    perms[real_path] = perm


def update_permission_rule(path, rule):
    return add_permission_rule(path, rule)


def add_ignore(target):
    target = Path(target).resolve()
    if target not in ignores:
        ignores.append(target)


def remove_ignore(target):
    target = Path(target).resolve()
    if target in ignores:
        ignores.remove(target)


def get_ignore():
    return ignores


def get_mounts():
    return mounts


def is_ignored(path):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return True
    
    for ignore in ignores:
        if real_path.is_relative_to(ignore):
            return True
    return False


def check_permission(path, user_id, permission):
    perm = get_file_permission(path, user_id)
    if perm is None:
        return False
    
    return pm.check_permission(perm, permission)


def create_folder(path, folder_name, user_id):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False
    
    if(not real_path.is_dir()):
        return False

    if not check_permission(path, user_id, 'a'):
        return False
    
    return fh.create_folder(real_path / folder_name)


def delete_file(path, user_id):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False
    
    if not check_permission(path, user_id, 'x'):
        return False
    
    return fh.delete_file(real_path)


def rename_file(path, new_name, user_id):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False
    
    if not check_permission(path, user_id, 'm'):
        return False
    
    return fh.rename_file(real_path, new_name)


def move_file(path, new_path, user_id):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False
    
    if not check_permission(path, user_id, 'm'):
        return False
    
    new_path = Path(new_path)
    new_real_path = get_file_real_path(new_path, check_exists=False)
    if new_real_path is None:
        return False
    
    if not check_permission(new_path.parent, user_id, 'a'):
        return False
    
    return fh.move_file(real_path, new_real_path)


def copy_file(path, new_path, user_id):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False
    
    if not check_permission(path, user_id, 'm'):
        return False
    
    new_path = Path(new_path)
    new_real_path = get_file_real_path(new_path, check_exists=False)
    if new_real_path is None:
        return False
    
    if not check_permission(new_path.parent, user_id, 'a'):
        return False
    
    return fh.copy_file(real_path, new_real_path)


def list_root_file(user_id):
    result = []
    for mount in mounts.values():
        root = mount['root']
        if root.count('/') > 1:
            continue
        if not user_visible(root, user_id):
            continue
        real_path = get_file_real_path(root)
        if real_path is None:
            continue
        result.append({
            'path': root,
            'type': 0 if real_path.is_dir() else 1,
        })

    return result


def list_file(user_id, parent):
    if parent == '/':
        return list_root_file(user_id)
    parent = Path(parent)
    real_path = get_file_real_path(parent)
    if real_path is None:
        return []
    if not real_path.is_dir():
        return []
    
    ls = os.listdir(str(real_path))
    result = []
    for f in ls:
        path = parent / f
        if user_visible(path, user_id):
            path = str(path).replace('\\', '/')
            real = real_path / f
            type = 0 if real.is_dir() else 1
            result.append({
                'path': path,
                'type': type,
            })
    return result


def share_file(path, share_options: dict):
    # TODO: 建立分享系统后再编写
    pass


def load_data():
    global mounts
    m = dsh.deserialize_mounts(None, load_path=cfg.mount_data_path)
    valid = True
    for mount in m.values():
        if not validate_mount(m['target'], m['root']):
            valid = False
            target = m['target']
            print(f'Mount {target} is invalid.')
            break
    if valid:
        mounts = m


def save_data():
    dsh.serialize_mounts(mounts, save_path=cfg.mount_data_path)
