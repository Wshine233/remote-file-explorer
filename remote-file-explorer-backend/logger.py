import crypto
import config as cfg


logs = [
    {
        # 示例
        'time': 1619433600,
        'level': 'info',
        'user': 'admin',
        'action': 'login',
        'message': 'Login success.',
        'data': {
            # 自定义数据
        }
    }
]


def load_data():
    pass


def save_data():
    # save时清理过期日志
    pass


def get_logs_by_user(user_id, time_after=0):
    """获取某用户的日志, time_after为0则不限制时间范围"""
    result = []
    for log in logs:
        if log['user'] == user_id and log['time'] >= time_after:
            result.append(log)
    return result


def log(level, user_id, action, message, data={}):
    """记录日志"""
    logs.append({
        'time': crypto.time(),
        'level': level,
        'user': user_id,
        'action': action,
        'message': message,
        'data': data
    })
    save_data()


def log_info(user_id, action, message, data={}):
    """记录info级别日志"""
    log('info', user_id, action, message, data)


def log_warning(user_id, action, message, data={}):
    """记录warning级别日志"""
    log('warning', user_id, action, message, data)


def log_important(user_id, action, message, data={}):
    """记录important级别日志"""
    log('important', user_id, action, message, data)


load_data()