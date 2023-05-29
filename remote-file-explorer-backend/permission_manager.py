import user_manager as um
import config as cfg


permission_groups = [
    {
        'id': 'admin',
        'permission': "adxms"  # a: add, d: download, x: delete, m: manage, s: share
    },
    {
        'id': 'restrict',
        'permission': "-----"
    }
]


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
    permission_groups.append({
        'id': id,
        'permission': permission
    })
    return True


def remove_group(id):
    for group in permission_groups:
        if group['id'] == id:
            permission_groups.remove(group)
            return True
    return False


def update_group(id, permission):
    group = get_group(id)
    if group is None:
        return False
    group['permission'] = permission
    return True


def get_default_group():
    return cfg.default_group


def check_permission(permission, check):
    if check not in 'adxms':
        return False
    # 如果包含权限继承，由于未提供上层权限，也记作无权限
    return check in permission