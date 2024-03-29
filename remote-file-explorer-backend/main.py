from flask import Flask, request, jsonify, send_file
import config as cfg
import user_manager as um
import response_helper as rh
import permission_manager as pm
import file_manager as fm
import crypto
import preview_helper as ph
from pathlib import Path
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/test/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'})



""" 用户请求部分 """

@app.route('/user/super', methods=['POST'])
def super():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        if session is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] in cfg.super_group:
            return rh.pack_response(True, 'Super user.', True)
        else:
            return rh.pack_response(True, 'Normal user.', False)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/user/list', methods=['POST'])
def list_users():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        keys = data.get('keys')
        if session is None or keys is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] in cfg.super_group:
            return rh.pack_response(True, 'Super user.', um.list_users(keys))
        else:
            return rh.pack_response(False, 'Permission denied.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/user/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        id = data.get('id')
        hash = data.get('hash')
        if id is None or hash is None:
            raise Exception('Request format error.')
        
        user = um.login(id, hash)
        print(user)
        if user is None:
            return rh.pack_response(False, 'Please check your id and password.')
        else:
            return rh.pack_response(True, 'Login success.', user)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/user/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        id = data.get('id')
        hash = data.get('hash')
        if id is None or hash is None:
            raise Exception('Request format error.')
        
        name = id
        permission_group = pm.get_default_group()
        permission = "*****"
        result = um.add_user(id, hash, name, permission_group, permission)
        if result:
            return rh.pack_response(True, 'Register success.')
        else:
            return rh.pack_response(False, 'User already exists.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)



@app.route('/user/session-login', methods=['POST'])
def session_login():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        if session is None:
            raise Exception('Request format error.')
        
        res = um.session_login(session)
        if res is None:
            return rh.pack_response(False, "Session Expired.")
        return rh.pack_response(True, "Login success.", res)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)



@app.route('/user/logout', methods=['POST'])
def logout():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        if session is None:
            raise Exception('Request format error.')
        
        um.logout(session)
        return rh.pack_response(True, 'Logout success.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/user/update-user', methods=['POST'])
def update_user():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        keys = data.get('keys')
        values = data.get('values')
        if session is None or keys is None or values is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        result = um.update_user(user, keys, values)
        if result:
            return rh.pack_response(True, 'Update user info success.')
        else:
            return rh.pack_response(False, 'Update user info failed.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/user/set-info', methods=['POST'])
def set_info():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        keys = data.get('keys')
        values = data.get('values')
        user_id = data.get('userId')
        if session is None or keys is None or values is None or user_id is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
            return rh.pack_response(False, 'Permission denied.')
        
        if user == user_id and 'permissionGroup' in keys:
            # 不能修改自己的权限组至非超级用户组，否则会导致无法管理信息
            if values[keys.index('permissionGroup')] not in cfg.super_group:
                return rh.pack_response(False, 'Cannot change your own permission group to non-super group.')
            
        
        result = um.update_user(user_id, keys, values)
        if result:
            return rh.pack_response(True, 'Update user info success.')
        else:
            return rh.pack_response(False, 'Update user info failed.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/user/remove', methods=['POST'])
def delete_user():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        user_id = data.get('userId')
        if session is None or user_id is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
            return rh.pack_response(False, 'Permission denied.')
        
        if user == user_id:
            return rh.pack_response(False, 'You cannot delete yourself.')
        
        result = um.remove_user(user_id)
        if result:
            return rh.pack_response(True, 'Delete user success.')
        else:
            return rh.pack_response(False, 'Delete user failed.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/user/update-password', methods=['POST'])
def update_password():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        old_password = data.get('oldHash')
        new_password = data.get('newHash')
        if session is None or old_password is None or new_password is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        result = um.update_password(user, old_password, new_password, session)
        if result:
            return rh.pack_response(True, 'Update password success.')
        else:
            return rh.pack_response(False, 'Update password failed. Old password incorrect.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/user/get-user', methods=['POST'])
def get_user():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        keys = data.get('keys')
        if session is None or keys is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        result = um.get_user_info(user, keys)
        if result is None:
            return rh.pack_response(False, 'User not found.')
        else:
            return rh.pack_response(True, 'Get user info success.', result)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/user/verify-session', methods=['POST'])
def verify_session():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        if session is None:
            raise Exception('Request format error.')
        if um.verify_session(session):
            return rh.pack_response(True, 'Session valid.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


""" 文件请求部分 """

@app.route('/file/info', methods=['POST'])
def get_file():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        paths = data.get('path')
        keys = data.get('keys')
        if session is None or paths is None or keys is None:
            raise Exception('Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        result = fm.get_file_info(paths, keys, user)
        if result is None:
            return rh.pack_response(False, 'File not found.')
        return rh.pack_response(True, f'Success. Got {len(result)} item(s).', result)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/file/list-file', methods=['POST'])
def list_file():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        path = data.get('path')
        if session is None or path is None:
            raise Exception('Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        result = fm.list_file(user, path)
        return rh.pack_response(True, f'Success. Got {len(result)} item(s).', result)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/file/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        keyword = data.get('keyword')
        filter = data.get('filter')
        
        if session is None or keyword is None or filter is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        result = fm.find_file(user, keyword, filter)
        return rh.pack_response(True, f'Success. Got {len(result)} item(s).', result)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)
        

@app.route('/file/check-perm', methods=['POST'])
def check_perm():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        path = data.get('path')
        perm = data.get('perm')
        if session is None or path is None or perm is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        result = fm.check_permission(path, user, perm)
        return rh.pack_response(True, 'Success.', result)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/file/download', methods=['GET'])
def download():
    try:
        session = request.args.get('sessionId')
        path = request.args.get('path')
        if session is None or path is None:
            raise Exception('Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        perm = fm.check_permission(path, user, 'd')
        if not perm:
            return rh.pack_response(False, "You don't have permission to download this file.")
        
        result = fm.get_file_real_path(path)
        if result is None:
            return rh.pack_response(False, 'File not found. Maybe it is a mount point.')

        return send_file(str(result), as_attachment=True)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/file/upload', methods=['POST'])
def upload():
    try:
        session = request.form.get('sessionId')
        root = request.form.get('root')
        files = request.files.getlist('files')
        if session is None or root is None or files is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        if root == '/':
            return rh.pack_response(False, "You cannot upload files to root '/'.")
        
        if not fm.check_permission(root, user, 'a'):
            return rh.pack_response(False, "You don't have permission to upload files to this directory.")
        
        root = Path(root)
        real_root = fm.get_file_real_path(root)
        if real_root is None:
            return rh.pack_response(False, 'Directory not found. Maybe it is a mount point.')
        
        link = []
        for file in files:
            filename = root / file.filename
            real_path = fm.get_file_real_path(filename)
            if real_path is not None:
                return rh.pack_response(False, f'File {file.filename} already exists.')
            real_path = fm.get_file_real_path(filename, check_exists=False)
            
            if real_path is None:
                return rh.pack_response(False, 'Unknown error. Cannot get real path.')
            if real_path.exists():
                return rh.pack_response(False, f'File {file.filename} already exists.')
            
            real_path.parent.mkdir(parents=True, exist_ok=True)
            link.append({
                'path': real_path,
                'file': file
            })

        for item in link:
            item['file'].save(str(item['path']))

        return rh.pack_response(True, 'Success.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)

@app.route('/file/delete', methods=['POST'])
def delete():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        paths = data.get('paths')
        if session is None or paths is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        result = fm.delete_files(paths, user)
        if result:
            return rh.pack_response(True, 'Success.')
        else:
            return rh.pack_response(False, 'Failed. Maybe you do not have permission to delete some files.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/file/create-folder', methods=['POST'])
def create_folder():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        path = data.get('path')
        name = data.get('name')
        if session is None or path is None:
            raise Exception('Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        result = fm.create_folder(path, name, user)
        if result:
            return rh.pack_response(True, 'Success.')
        else:
            return rh.pack_response(False, 'Failed. Folder already exists, or you do not have permission to create folder here.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/file/rename', methods=['POST'])
def rename():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        path = data.get('path')
        name = data.get('name')
        if session is None or path is None or name is None:
            raise Exception('Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        if fm.is_mount_point(path):
            return rh.pack_response(False, 'Failed. You cannot rename a mount point.')

        result = fm.rename_file(path, name, user)
        if result:
            return rh.pack_response(True, 'Success.')
        else:
            return rh.pack_response(False, 'Failed. Check if there is a file with the same name, or you do not have permission to rename this file.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)



@app.route('/file/copy-move', methods=['POST'])
def copy_move():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        files = data.get('files')
        new_parent = data.get('newParent')
        if session is None or files is None or new_parent is None:
            return rh.pack_response(False, 'Request format error.')
        if not isinstance(files, list) or len(files) == 0 or not isinstance(new_parent, str):
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        result = fm.copy_move_files(files, new_parent, user)
        # 获得成功和失败的任务个数
        success = 0
        failed = 0
        for item in result:
            if item['success']:
                success += 1
            else:
                failed += 1

        return rh.pack_response(True, f'Result of tasks, got {success} succeed and {failed} faild', result)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)



@app.route('/file/share', methods=['POST'])
def share():
    pass


@app.route('/file/cancel-share', methods=['POST'])
def cancel_share():
    pass


@app.route('/file/get-share', methods=['POST'])
def get_share():
    pass


@app.route('/file/manage', methods=['POST'])
def manage():
    pass


@app.route('/file/rule', methods=['POST'])
def rule():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        path = data.get('path')
        if session is None or path is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
            return rh.pack_response(False, 'Permission denied.')
        
        real_path = fm.get_file_real_path(path)
        if real_path is None:
            return rh.pack_response(False, 'File not found.')
        
        result = fm.perms.get(real_path, None)
        if result is None:
            return rh.pack_response(True, 'Perm not found, but generate a new default perm.', fm.generate_default_permission(path))
        else:
            return rh.pack_response(True, 'Successfully found perm.', result)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/file/set-rule', methods=['POST'])
def set_rule():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        path = data.get('path')
        rule = data.get('rule')
        if session is None or path is None or rule is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
            return rh.pack_response(False, 'Permission denied.')
        
        real_path = fm.get_file_real_path(path)
        if real_path is None:
            return rh.pack_response(False, 'File not found.')
        
        if not fm.validate_perm_info(rule):
            return rh.pack_response(False, 'Invalid rule format.')
        
        for invisibleUser in rule['invisibleUser']:
            info = um.get_user_by_id(invisibleUser)
            if info is not None and info['permissionGroup'] in cfg.super_group:
                return rh.pack_response(False, 'Cannot set invisible to super user.')

        result = fm.set_perm_info(rule)
        if not result:
            return rh.pack_response(False, 'Failed.')

        return rh.pack_response(True, 'Success.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/file/perm', methods=['POST'])
def get_perm():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        paths = data.get('paths')
        if session is None or paths is None:
            raise Exception('Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        result = []
        for path in paths:
            result.append({
                'path': path,
                'perm': fm.get_file_permission(path, user)
            })
        if result is None:
            return rh.pack_response(False, 'File not found.')
        return rh.pack_response(True, 'Success.', result)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


"""预览部分"""
@app.route('/preview/token', methods=['POST'])
def preview_token():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        path = data.get('path')
        ip = request.remote_addr

        if session is None or path is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        token = crypto.preview_token(user, path, ip)
        if token is None:
            return rh.pack_response(False, 'Cannot get token.')
        return rh.pack_response(True, 'Success.', token)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/preview', methods=['GET'])
def preview():
    try:
        token = request.args.get('token')
        session = request.args.get('user')
        ip = request.remote_addr
        
        if token is None or session is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        

        result = ph.get_preview_file(token, user, ip)
        if result is None:
            return rh.pack_response(False, 'Preview Not Found.')
        return send_file(result, as_attachment=False)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


"""挂载部分"""

@app.route('/mount', methods=['POST'])
def get_mount():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        if session is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
            return rh.pack_response(False, 'Permission denied.')
        
        result = fm.get_mounts()
        if result is None:
            return rh.pack_response(True, 'Mount not found.', [])
        return rh.pack_response(True, 'Success.', result)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/mount/add', methods=['POST'])
def add_mount():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        real_path = data.get('target')   # 真实绝对路径
        mount_path = data.get('root')  # 挂载后的路径
        if session is None or real_path is None or mount_path is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')

        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
            return rh.pack_response(False, 'Permission denied.')
        
        real_path = Path(real_path)
        if not real_path.exists():
            return rh.pack_response(False, 'File not found.')
        
        result = fm.add_mount(real_path, mount_path)
        if not result:
            return rh.pack_response(False, 'Mount failed. Try another mount root.')
        return rh.pack_response(True, 'Success.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/mount/remove', methods=['POST'])
def remove_mount():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        mount_path = data.get('root')  # 挂载后的路径
        if session is None or mount_path is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')

        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
            return rh.pack_response(False, 'Permission denied.')
        
        real_path = fm.get_file_real_path(mount_path)
        if real_path is None:
            return rh.pack_response(False, 'Mount Target not found.')
        
        result = fm.remove_mount(real_path)
        if not result:
            return rh.pack_response(False, 'Mount not found.')
        return rh.pack_response(True, 'Success.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)
    

"""忽略列表部分"""

@app.route('/ignore', methods=['POST'])
def get_ignore():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        if session is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
            return rh.pack_response(False, 'Permission denied.')
        
        result = fm.get_ignore()
        if result is None:
            return rh.pack_response(True, 'Ignore not found.', [])
        return rh.pack_response(True, 'Success.', result)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/ignore/add', methods=['POST'])
def add_ignore():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        path = data.get('target')  # 真实绝对路径
        if session is None or path is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')

        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
            return rh.pack_response(False, 'Permission denied.')
        
        path = Path(path)
        if not path.exists():
            return rh.pack_response(False, 'File not found.')
        
        result = fm.add_ignore(path)
        if not result:
            return rh.pack_response(False, 'Ignore failed. Try another ignore path.')
        return rh.pack_response(True, 'Success.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/ignore/adds', methods=['POST'])
def add_ignores():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        paths = data.get('paths') 
        if session is None or paths is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')

        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
            return rh.pack_response(False, 'Permission denied.')
        
        result = []
        for path in paths:
            result.append({
                'path': path,
                'success': fm.add_ignore_by_path(path)
            })
        return rh.pack_response(True, 'Success.', result)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/ignore/remove', methods=['POST'])
def remove_ignore():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        path = data.get('target')  # 真实绝对路径
        if session is None or path is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')

        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
            return rh.pack_response(False, 'Permission denied.')
        
        result = fm.remove_ignore(path)
        if not result:
            return rh.pack_response(False, 'Ignore not found.')
        return rh.pack_response(True, 'Success.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


"""权限部分"""

@app.route('/perm/list', methods=['POST'])
def get_perm_groups():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        if session is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')
        
        # if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
        #     return rh.pack_response(False, 'Permission denied.')
        
        result = pm.permission_groups
        if result is None:
            return rh.pack_response(True, 'Permission group not found.', [])
        return rh.pack_response(True, 'Success.', result)
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/perm/add', methods=['POST'])
def add_perm_group():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        name = data.get('id')
        perm = data.get('perm')
        if session is None or name is None or perm is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')

        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
            return rh.pack_response(False, 'Permission denied.')
        
        result = pm.add_group(name, perm)
        if not result:
            return rh.pack_response(False, 'Permission group already exists. Or your perm format is wrong.')
        return rh.pack_response(True, 'Success.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/perm/remove', methods=['POST'])
def remove_perm_group():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        name = data.get('id')
        if session is None or name is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')

        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
            return rh.pack_response(False, 'Permission denied.')
        
        if name == pm.get_default_group():
            return rh.pack_response(False, 'Cannot remove default group.')
        
        result = pm.remove_group(name)
        if not result:
            return rh.pack_response(False, 'Permission group not found.')
        return rh.pack_response(True, 'Success.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)


@app.route('/perm/update', methods=['POST'])
def update_perm_group():
    try:
        data = request.get_json()
        session = data.get('sessionId')
        name = data.get('id')
        perm = data.get('perm')
        if session is None or name is None or perm is None:
            return rh.pack_response(False, 'Request format error.')
        
        user = um.verify_session(session)
        if user:
            user = um.get_user_id(session)
            if user is None:
                return rh.pack_response(False, 'Unknown error. User not found.')
        else:
            return rh.pack_response(False, 'Session expired. Please login again.')

        if um.get_user_info(user, ['permissionGroup'])['permissionGroup'] not in cfg.super_group:
            return rh.pack_response(False, 'Permission denied.')
        
        result = pm.update_group(name, perm)
        if not result:
            return rh.pack_response(False, 'Permission group not found. Or your perm format is wrong.')
        return rh.pack_response(True, 'Success.')
    except Exception as e:
        return rh.pack_response(False, 'Request error.', e)




if __name__ == '__main__':
    if cfg.use_ssl:
        app.run(debug=False, host=cfg.host, port=cfg.port, ssl_context=cfg.ssl_context)
    else:
        app.run(debug=False, host=cfg.host, port=cfg.port)