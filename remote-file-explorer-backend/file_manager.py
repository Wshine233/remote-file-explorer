import permission_manager as pm
import user_manager as um
from pathlib import Path
import os
import config as cfg
import file_helper as fh
import data_serialize_helper as dsh
import search_helper as sh


# 挂载列表
mounts = {}

# {
#     Path('D:/Unity 3D/Projects'): {
#         'target': 'D:/Unity 3D/Projects',   # 被挂载的目录/文件位置，必须是绝对路径且唯一；启动时会检查是否存在；
#         'root': '/Unity 3D/Unity 项目',   # 挂载到的路径，必须以/开头，且唯一；一个挂载点只能挂载一个目录/文件; 不能直接挂载到'/'
#     },
#     Path('D:/_Pictures/【图片】'): {
#         'target': 'D:/_Pictures/【图片】',
#         'root': '/我的图片',
#     }
# }

# 文件权限列表
perms = {}

# {
#     Path('D:/Unity 3D/Projects'): {
#         'file': 'D:/Unity 3D/Projects',   # 目标目录/文件的绝对路径
#         'visibleGroup': ['super', 'admin', 'restrict'],   # 可见的权限组
#         'visibleUser': ['admin'],   # 可见的用户，覆盖权限组规则
#         'invisibleUser': ['user1'],   # 不可见的用户，覆盖权限组规则
#         'rules': [
#             {
#                 'type': 0,   # 0为权限组规则，1为用户规则
#                 'target': 'admin',   # 目标权限组/用户
#                 'permission': '**-**',   # 权限
#             },
#             {
#                 'type': 0,
#                 'target': 'restrict',
#                 'permission': 'adxms'
#             }
#         ]
#     },
#     Path('D:/_Pictures/【图片】'): {
#         'file': 'D:/_Pictures/【图片】',
#         'visibleGroup': ['super', 'admin', 'restrict'],
#         'visibleUser': ['admin'],
#         'invisibleUser': ['user1'],
#         'rules': [
#             {
#                 'type': 0,
#                 'target': 'admin',
#                 'permission': '**-**'
#             },
#             {
#                 'type': 0,
#                 'target': 'restrict',
#                 'permission': '-----'
#             }
#         ]
#     },
#     Path('D:/_Pictures/【图片】/download/你看不见我哦♡'): {
#         'file': 'D:/_Pictures/【图片】/download/你看不见我哦♡',
#         'visibleGroup': [],
#         'visibleUser': [],
#         'invisibleUser': [],
#         'rules': []
#     },
#     Path('D:/_Pictures/【图片】/测试'): {
#         'file': 'D:/_Pictures/【图片】/测试',
#         'visibleGroup': ['super', 'admin', 'restrict'],
#         'visibleUser': ['admin'],
#         'invisibleUser': ['user1'],
#         'rules': [
#             {
#                 'type': 0,
#                 'target': 'admin',
#                 'permission': '*****'
#             },
#             {
#                 'type': 0,
#                 'target': 'restrict',
#                 'permission': '-----'
#             }
#         ]
#     },
# }

# 忽略列表（使用绝对路径）
ignores = []

# [
#     Path('D:/test/ignore').resolve()
# ]



def load_data():
    # 读取mount列表
    global mounts
    cache = mounts
    mounts = {}
    m = dsh.deserialize_mounts(None, load_path=cfg.mount_data_path, defaultValue=dsh.format_mounts(cache))
    valid = True
    for mount in m.values():
        if not validate_mount(mount['target'], mount['root']):
            valid = False
            target = mount['target']
            print(f'Mount {target} is invalid.')
            break
    if valid:
        mounts = m
    else:
        mounts = cache
    
    # 读取权限列表
    global perms
    perms = dsh.deserialize_perms(None, load_path=cfg.perm_data_path, defaultValue=dsh.format_perms(perms))

    # 读取忽略列表
    global ignores
    ignores = dsh.deserialize_ignores(None, load_path=cfg.ignore_data_path, defaultValue=dsh.format_ignores(ignores))


def save_data():
    dsh.serialize_mounts(mounts, save_path=cfg.mount_data_path)
    dsh.serialize_perms(perms, save_path=cfg.perm_data_path)
    dsh.serialize_ignores(ignores, save_path=cfg.ignore_data_path)


def get_files_from_mounts(target: Path):
    """根据mounts挂载的path列表推断出指定路径下有哪些文件 

    这些文件都是挂载时形成的，可能实际并不存在，但需要一个虚拟路径。
    例如: 假设挂载列表里只有一个挂载, 将D:/folder目录挂载到了/test/test_folder目录。
    此时, /test/test_folder目录是可以被正常映射至D:/folder的, /test目录则无法找到映射, 因为它本身并没有作为其它文件的挂载点。
    但由于有目录挂载到了/test的子目录, 所以/test也必须在文件列表中存在
    """
    target = Path(target)
    result = []
    paths = [Path(mount['root']) for mount in mounts.values()]
    for path in paths:
        if path.parent.is_relative_to(target):
            real_path = get_file_real_path(path)
            if real_path is None:
                continue

            is_dir = real_path.is_dir()
            while path.parent.resolve() != target.resolve():
                is_dir = True
                path = path.parent
            result.append({
                'name': path.name,
                'type': 0 if is_dir else 1
            })
    return result


def get_file_real_path(path, check_exists=True):
    path = Path(path)
    for mount in mounts.values():
        root = Path(mount['root'])
        if fh.same_path(path, root):
            real = Path(mount['target'])
            return real.resolve() if not check_exists or real.exists() else None
        
        if path.is_relative_to(root):
            real = Path(mount['target']) / path.relative_to(mount['root'])
            if check_exists and not real.exists():
                continue
            return real.resolve()
    return None


def validate_mount(target: Path, root):
    target = Path(target)
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


def get_mounts():
    return list(mounts.values())


def add_mount(target: Path, root: str):
    if not validate_mount(target, root):
        return False

    mounts[target.resolve()] = {
        'target': str(target.resolve()).replace('\\', '/'),
        'root': root.replace('\\', '/')
    }

    if target in ignores:
        ignores.remove(target)
    
    perms[target.resolve()] = generate_default_permission(root)
    save_data()

    return True


def remove_mount(target: Path):
    if target not in mounts:
        return False

    del mounts[target.resolve()]
    del perms[target.resolve()]
    save_data()

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


def is_mount_point(root: str):
    # 检查指定路径是否为挂载点
    for mount in mounts.values():
        if fh.same_path(Path(root), Path(mount['root'])):
            return True


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


def user_visible_by_parent(path, user_id, parent_visible: bool):
    """事先得到父目录是否可见的结果，避免重复计算"""
    if not parent_visible:
        return False
    
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
    
    if real_path in perms:
        file_perm = perms[real_path]
        group_test = user_group in file_perm['visibleGroup']
        user_test = user_id in file_perm['visibleUser']
        block_test = user_id in file_perm['invisibleUser']
        if not block_test and (group_test or user_test):
            # 文件可以看见
            return True
        # 文件不可见
        return False
    # 文件没有权限设置，使用父目录的结果
    return parent_visible


def get_file_permission(path, user_id):
    """获取指定文件的权限"""
    path = Path(path)
    real_path = get_file_real_path(path, check_exists=False)
    if real_path is None:
        return '-----'

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


def get_file_permission_by_parent(path, user_id, parent_perm: str, real_path=None, parent_visible=None, visible=None):
    """获取指定文件的权限，事先得到父目录的权限，避免重复计算"""
    path = Path(path)
    if real_path is None:
        real_path = get_file_real_path(path, check_exists=False)
    if real_path is None:
        return '-----'

    user_info = um.get_user_info(user_id, ['permission', 'permissionGroup'])
    user_perm = user_info['permission']
    user_group = user_info['permissionGroup']
    group_perm = pm.get_group_permission(user_group)
    
    if visible is None:
        visible = user_visible_by_parent(path, user_id, parent_visible)
    if not visible:
        return "-----"
    
    perm = parent_perm
    if real_path not in perms:
        return perm
    
    file_perm = perms[real_path]
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


def get_file_info(paths: list, keys: list, user_id: str):
    ls = []
    for path in paths:
        real_path = get_file_real_path(path)
        if real_path is None:
            info = {'path': path}
            for key in keys:
                info[key] = None
            ls.append(info)
            continue
        
        info = {}
        info['path'] = path
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
        'visibleGroup': cfg.super_group.copy(),
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

    format_perm_info(result)

    return result


def validate_perm_info(perm):
    if 'file' not in perm or not isinstance(perm['file'], str):
        return False
    if 'visibleGroup' not in perm or not isinstance(perm['visibleGroup'], list):
        return False
    if 'visibleUser' not in perm or not isinstance(perm['visibleUser'], list):
        return False
    if 'invisibleUser' not in perm or not isinstance(perm['invisibleUser'], list):
        return False
    if 'rules' not in perm or not isinstance(perm['rules'], list):
        return False
    
    for group in perm['visibleGroup']:
        if not isinstance(group, str):
            return False
    for user in perm['visibleUser']:
        if not isinstance(user, str):
            return False
    for user in perm['invisibleUser']:
        if not isinstance(user, str):
            return False
    for rule in perm['rules']:
        if not isinstance(rule, dict):
            return False
        if 'type' not in rule or not isinstance(rule['type'], int):
            return False
        if 'target' not in rule or not isinstance(rule['target'], str):
            return False
        if 'permission' not in rule or not isinstance(rule['permission'], str) or not pm.validate_permission(rule['permission']):
            return False
    return True


def format_perm_info(perm):
    perm['file'] = str(Path(perm['file']).resolve())
    perm['visibleGroup'] += cfg.super_group
    perm['visibleGroup'] = list(set(perm['visibleGroup']))
    perm['visibleUser'] = list(set(perm['visibleUser']))
    perm['invisibleUser'] = list(set(perm['invisibleUser']))

    for group in perm['visibleGroup'][:]:
        if pm.get_group(group) is None:
            perm['visibleGroup'].remove(group)
    for user in perm['visibleUser'][:]:
        if um.get_user_by_id(user) is None:
            perm['visibleUser'].remove(user)
    for user in perm['invisibleUser'][:]:
        if um.get_user_by_id(user) is None:
            perm['invisibleUser'].remove(user)


def set_perm_info(perm):
    if not validate_perm_info(perm):
        return False
    real_path = Path(perm['file']).resolve()
    if not real_path.exists():
        return False
    
    format_perm_info(perm)
    perms[real_path] = perm
    save_data()
    return True


def update_rule(perm, rule):
    for r in perm['rules']:
        if r['type'] == rule['type'] and r['target'] == rule['target']:
            r['permission'] = rule['permission']
    perm['rules'].append(rule)
    save_data()


def remove_rule(perm, type, target):
    for r in perm['rules']:
        if r['type'] == type and r['target'] == target:
            perm['rules'].remove(r)
    save_data()


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
    save_data()


def remove_permission_rule(path, type, target):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False
    
    perm = get_permission(path, generate_default_permission(path))
    remove_rule(perm, type, target)
    perms[real_path] = perm
    save_data()


def update_permission_rule(path, rule):
    return add_permission_rule(path, rule)


def add_visibility_rule(path, key: str, value: str):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False
    
    perm = perms[real_path]
    if key not in perm:
        return False
    if value in perm[key]:
        return False
    perm[key].append(value)
    save_data()


def remove_visibility_rule(path, key: str, value: str):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False
    
    perm = perms[real_path]
    if key not in perm:
        return False
    if value not in perm[key]:
        return False
    perm[key].remove(value)
    save_data()


def get_file_perm_info(path):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return None
    
    perm = perms.get(real_path, None)
    return perm


def add_ignore(target):
    target = Path(target).resolve()
    if target not in ignores:
        ignores.append(target)
        save_data()
        return True
    return False


def add_ignore_by_path(path):
    real_path = get_file_real_path(path)
    if real_path is None:
        return False
    return add_ignore(real_path)        


def remove_ignore(target):
    target = Path(target).resolve()
    if target in ignores:
        ignores.remove(target)
        save_data()
        return True
    return False


def get_ignore():
    return [str(ignore) for ignore in ignores]


def get_mounts():
    return list(mounts.values())


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


def delete_files(paths, user_id):
    for path in paths:
        if not check_permission(path, user_id, 'x'):
            return False
    
    for path in paths:
        delete_file(path, user_id)

    return True


def rename_file(path, new_name, user_id):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False
    
    if not check_permission(path, user_id, 'm'):
        return False
    
    return fh.rename_file(real_path, new_name)


def move_file(path, new_parent, user_id):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False, True, 'Cannot locate real path.'   # 无法定位到原文件，该任务已无作用，可以删除
    
    if not check_permission(path, user_id, 'm'):
        return False, True, 'No modify permission.'   # 无权修改原文件，该任务已无作用，可以删除
    if not check_permission(new_parent, user_id, 'a'):
        return False, False, 'No add permission.'   # 无权在新目录下创建文件，但可以换一个目录粘贴，该任务仍然有效，不可删除
    if not check_permission(path, user_id, 'x'):
        return False, True, 'No delete permission.'   # 无权删除原文件，该任务已无作用，可以删除
    
    new_path = Path(new_parent) / path.name
    new_real_path = get_file_real_path(new_path, check_exists=False)
    if new_real_path is None:
        return False, False, 'Cannot locate to target real path.'  # 无法定位到新的目录，但可以换一个目录粘贴，该任务仍然有效，不可删除
    
    return fh.move_file(real_path, new_real_path)


def check_move_file(path, new_parent, user_id):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False, True, 'Cannot locate real path.'   # 无法定位到原文件，该任务已无作用，可以删除
    
    if not check_permission(path, user_id, 'm'):
        return False, True, 'No modify permission.'   # 无权修改原文件，该任务已无作用，可以删除
    if not check_permission(new_parent, user_id, 'a'):
        return False, False, 'No add permission in target path.'  # 无权在新目录下创建文件，但可以换一个目录粘贴，该任务仍然有效，不可删除
    if not check_permission(path, user_id, 'x'):
        return False, True, 'No delete permission.'   # 无权删除原文件，该任务已无作用，可以删除
    
    new_path = Path(new_parent) / path.name
    new_real_path = get_file_real_path(new_path, check_exists=False)
    if new_real_path is None:
        return False, False, 'Cannot locate to target real path.'  # 无法定位到新的目录，但可以换一个目录粘贴，该任务仍然有效，不可删除
    
    return fh.check_copy_move(real_path, new_real_path)


def copy_file(path, new_parent, user_id):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False, True, 'Cannot locate real path.'   # 无法定位到原文件，该任务已无作用，可以删除
    
    if not check_permission(path, user_id, 'm'):
        return False, True, 'No modify permission.'   # 无权修改原文件，该任务已无作用，可以删除
    if not check_permission(new_parent, user_id, 'a'):
        return False, False, 'No add permission in target path.'  # 无权在新目录下创建文件，但可以换一个目录粘贴，该任务仍然有效，不可删除
    
    new_path = Path(new_parent) / path.name
    new_real_path = get_file_real_path(new_path, check_exists=False)
    if new_real_path is None:
        return False, False, 'Cannot locate to target real path.'  # 无法定位到新的目录，但可以换一个目录粘贴，该任务仍然有效，不可删除
    
    return fh.copy_file(real_path, new_real_path)


def check_copy_file(path, new_parent, user_id):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False, True, 'Cannot locate real path.'   # 无法定位到原文件，该任务已无作用，可以删除
    
    if not check_permission(path, user_id, 'm'):
        return False, True, 'No modify permission.'   # 无权修改原文件，该任务已无作用，可以删除
    if not check_permission(new_parent, user_id, 'a'):
        return False, False, 'No add permission in target path.'  # 无权在新目录下创建文件，但可以换一个目录粘贴，该任务仍然有效，不可删除
    
    new_path = Path(new_parent) / path.name
    new_real_path = get_file_real_path(new_path, check_exists=False)
    if new_real_path is None:
        return False, False, 'Cannot locate to target real path.'  # 无法定位到新的目录，但可以换一个目录粘贴，该任务仍然有效，不可删除
    
    return fh.check_copy_move(real_path, new_real_path)


def copy_move_files(files: list, new_parent, user_id):
    """根据每条任务的类型判断是移动还是拷贝，最终返回每条任务的结果
    返回结构：
    [
        {
            'path': 'xxx',
            'mode': 'copy'/'move',
            'success': True/False,
            'message': 'xxx',
            'cancel': True/False
        }
    ]

    path: 任务的原路径
    mode: 任务的类型，拷贝或移动
    success: 任务是否成功
    message: 任务的结果描述
    cancel: 任务是否已无作用，可删除。一些任务虽然失败，但可以保留，比如无权在目标目录下创建文件，但可以换一个目录粘贴。

    参数中files结构:
    [
        {
            'path': 'xxx',
            'mode': 'copy'/'move'
        }
    ]

    path: 任务的原路径
    mode: 任务的类型，拷贝或移动
    
    预处理时，先过滤掉无效的任务，比如无法定位到原文件的任务，无权修改原文件的任务，无权在目标目录下创建文件的任务。
    处理时，先将所有任务按照路径排序，越深的路径越靠前，这样可以保证先处理子目录再处理父目录。
    """

    new_parent = Path(new_parent)
    results = []
    tasks = []

    for file in files:
        if file['mode'] == 'move':
            success, cancel, message = check_move_file(file['path'], new_parent, user_id)
            if success:
                tasks.append(file)
            else:
                results.append({
                    'path': file['path'],
                    'mode': 'move',
                    'success': False,
                    'message': message,
                    'cancel': cancel
                })
        elif file['mode'] == 'copy':
            success, cancel, message = check_copy_file(file['path'], new_parent, user_id)
            if success:
                tasks.append(file)
            else:
                results.append({
                    'path': file['path'],
                    'mode': 'copy',
                    'success': False,
                    'message': message,
                    'cancel': cancel
                })
        else:
            results.append({
                'path': file['path'],
                'mode': file['mode'],
                'success': False,
                'message': 'Unknown mode.',
                'cancel': True
            })

    tasks.sort(key=lambda x: len(get_file_real_path(x['path']).parents), reverse=True)

    for task in tasks:
        if task['mode'] == 'move':
            success, cancel, message = move_file(task['path'], new_parent, user_id)
            results.append({
                'path': task['path'],
                'mode': 'move',
                'success': success,
                'message': message,
                'cancel': cancel
            })
        elif task['mode'] == 'copy':
            success, cancel, message = copy_file(task['path'], new_parent, user_id)
            results.append({
                'path': task['path'],
                'mode': 'copy',
                'success': success,
                'message': message,
                'cancel': cancel
            })
        else:
            results.append({
                'path': task['path'],
                'mode': task['mode'],
                'success': False,
                'message': 'Unknown mode.',
                'cancel': True
            })

    return results
    



def list_root_file(user_id):
    result = {}
    
    for file in get_files_from_mounts(Path('/')):
        path = '/' + file['name']
        real_path = get_file_real_path(path)
        if real_path is not None and not user_visible('/'+ file['name'], user_id):
            continue

        time = None
        size = None
        time_created = None
        if real_path is not None:
            time = fh.get_file_last_modified(real_path)
            size = fh.get_file_size(real_path)
            time_created = fh.get_file_created(real_path)
        
        perm = get_file_permission_by_parent(path, user_id, '-----',
                                             real_path=real_path, parent_visible=True,
                                             visible=True)

        result[path] = {
            'path': path,
            'type': file['type'],
            'time': time,
            'time_created': time_created,
            'size': size,
            'perm': perm
        }
    
    result = list(result.values())
    result.sort(key=lambda x: str(x['path']))

    return result


def list_file(user_id, parent):
    if parent == '/':
        return list_root_file(user_id)
    parent = Path(parent)
    real_path = get_file_real_path(parent)
    if real_path is not None and not real_path.is_dir():
        return []
    
    result = {}
    if real_path is not None:
        ls = os.listdir(str(real_path))
        parent_visible = user_visible(parent, user_id)
        parent_perm = get_file_permission(parent, user_id)
        for f in ls:
            try:
                path = parent / f
                if user_visible_by_parent(path, user_id, parent_visible):
                    path = fh.to_path_str(path)
                    real = real_path / f
                    type = 0 if real.is_dir() else 1

                    time = None
                    time_created = None
                    size = None
                    if real is not None:
                        time = fh.get_file_last_modified(real)
                        time_created = fh.get_file_created(real)
                        size = fh.get_file_size(real)
                    
                    perm = get_file_permission_by_parent(path, user_id, parent_perm, real_path=real, parent_visible=parent_visible, visible=True)

                    result[path] = {
                        'path': path,
                        'type': type,
                        'time': time,
                        'time_created': time_created,
                        'size': size,
                        'perm': perm
                    }
            except:
                pass
    
    for file in get_files_from_mounts(parent):
        path = str(parent / file['name']).replace('\\', '/')
        real = get_file_real_path(path)

        time = None
        time_created = None
        size = None
        perm = '-----'
        if real is not None:
            if not user_visible_by_parent(path, user_id, True):
                continue
            size = fh.get_file_size(real)
            time = fh.get_file_last_modified(real)
            time_created = fh.get_file_created(real)
            perm = get_file_permission_by_parent(path, user_id, '-----', real_path=real, parent_visible=True, visible=True)

        result[path] = {
            'path': path,
            'type': file['type'],
            'time': time,
            'time_created': time_created,
            'size': size,
            'perm': perm  # 挂载路径是虚拟的，没有权限
        }
    
    result = list(result.values())
    if len(result) > 0:
        result.sort(key=lambda x: str(x['path']))

    return result


def get_file_type(path):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return None
    
    if real_path.is_dir():
        return 0
    else:
        return 1


def get_file_size(path):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return None
    
    return fh.get_file_size(real_path)


def get_file_time_modified(path):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return None
    
    return fh.get_file_last_modified(real_path)


def get_search_result_unit(file):
    return {
        'path': file['path'],
        'name': file['path'].split('/')[-1],
        'type': file['type'],
        'time_modified': file['time'],
        'time_created': file['time_created'],
        'size': file['size'],
        'perm': file['perm']
    }


def find_file_in_path(user_id, keyword, path, recursive=False):
    path = Path(path)
    print(f"Finding file in path: {path}")
    
    files = list_file(user_id, path)
    result = []
    for file in files:
        if recursive and file['type'] == 0:
            result += find_file_in_path(user_id, keyword, file['path'], recursive)
        
        if keyword in file['path'].split('/')[-1]:
            result.append(get_search_result_unit(file))

    return result
    

def find_file(user_id, keyword, filter: dict):
    if filter.get('folder', None) is None:
        filter['folder'] = '/'
    if filter.get('recursive', None) is None:
        filter['recursive'] = False
    if filter.get('type', None) is None:
        filter['type'] = [0, 1]
    
    result = find_file_in_path(user_id, keyword, filter['folder'], recursive=filter['recursive'])
    result = sh.filter_type(result, filter['type'])

    if filter.get('ext', None) is not None:
        result = sh.filter_extention(result, filter['ext'], 0 in filter['type'], filter['ext_blacklist'])
    if filter.get('time_modified', None) is not None:
        result = sh.filter_modified_time(result, filter['time_modified'][0], filter['time_modified'][1])
    if filter.get('time_created', None) is not None:
        result = sh.filter_created_time(result, filter['time_created'][0], filter['time_created'][1])
    
    return result


def file_exist(path):
    path = Path(path)
    real_path = get_file_real_path(path)
    if real_path is None:
        return False
    
    return real_path.exists()



load_data()