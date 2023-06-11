import user_manager as um
import data_serialize_helper as dsh
import config as cfg


permission_groups = [
    {
        'id': 'super',
        'permission': "adxms"
    },
    {
        'id': 'admin',
        'permission': "adxms"  # a: add, d: download, x: delete, m: manage, s: share
    },
    {
        'id': 'restrict',
        'permission': "-----"
    },
    
]


def load_data():
    global permission_groups
    permission_groups = dsh.deserialize_groups(None, cfg.permission_group_path, defaultValue=dsh.format_groups(permission_groups))


def save_data():
    dsh.serialize_groups(permission_groups, cfg.permission_group_path)


def get_group_permission(id):
    for group in permission_groups:
        if group['id'] == id:
            return group['permission']
    return None


def get_group(id):
    for group in permission_groups:
        if group['id'] == id:
            return group
    return None


def merge_permission(parent, child):
    if parent is None or child is None:
        return None
    if len(parent) != len(child):
        return None
    result = ''
    for i in range(len(parent)):
        if child[i] == '*':
            result += parent[i]
        else:
            result += child[i]
    return result


def get_user_permission(user_id):
    """根据用户所在权限组和用户自身权限计算用户的权限"""
    user = um.get_user_by_id(user_id)
    if user is None:
        return None
    group_permission = get_group_permission(user['permissionGroup'])
    if group_permission is None:
        group_permission = get_group_permission(cfg.default_group)
    if group_permission is None:
        return None
    return merge_permission(group_permission, user['permission'])


def add_group(id, permission):
    if get_group_permission(id) is not None:
        return False
    
    if not validate_permission(permission, allow_inherit=False):
        return False
    
    permission_groups.append({
        'id': id,
        'permission': permission
    })
    save_data()
    return True


def remove_group(id):
    for group in permission_groups:
        if group['id'] == id:
            permission_groups.remove(group)
            save_data()
            return True
    return False


def update_group(id, permission):
    group = get_group(id)
    if group is None:
        return False
    
    if not validate_permission(permission, allow_inherit=False):
        return False

    group['permission'] = permission
    save_data()
    return True


def get_default_group():
    return cfg.default_group


def check_permission(permission, check):
    if check not in 'adxms':
        return False
    # 如果包含权限继承，由于未提供上层权限，也记作无权限
    return check in permission


def validate_permission(perm, allow_inherit=True):
    if perm is None:
        return False
    if len(perm) != 5:
        return False
    if perm[0] not in ('a*-' if allow_inherit else 'a-'):
        return False
    if perm[1] not in ('d*-' if allow_inherit else 'd-'):
        return False
    if perm[2] not in ('x*-' if allow_inherit else 'x-'):
        return False
    if perm[3] not in ('m*-' if allow_inherit else 'm-'):
        return False
    if perm[4] not in ('s*-' if allow_inherit else 's-'):
        return False
    return True


load_data()
if get_group(get_default_group()) is None:
    add_group(get_default_group(), '-----')