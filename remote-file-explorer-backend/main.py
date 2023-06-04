from flask import Flask, request, jsonify, send_file
import config as cfg
import user_manager as um
import response_helper as rh
import permission_manager as pm
import file_manager as fm
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/test/hello')
def data():
    if request.method == 'GET':
        # 处理 GET 请求
        return jsonify({'message': 'Hello, World!'})
    elif request.method == 'POST':
        # 处理 POST 请求
        data = request.get_json()
        name = data.get('name')
        age = data.get('age')
        return jsonify({'message': f'Hello, {name}! You are {age} years old.'})
    return jsonify({'message': 'Hello, World!'})


@app.route('/test/download', methods=['GET'])
def test_download():
    return send_file("D:/[]临时工作间/[Mabors-Sub][Fate stay night Heaven's Feel III.spring song][Movie][720P][GB][BDrip][AVC AAC YUV420P8].mp4", as_attachment=True)


""" 用户请求部分 """

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
    pass


@app.route('/user/delete-user', methods=['POST'])
def delete_user():
    pass


@app.route('/user/update-password', methods=['POST'])
def update_password():
    pass


@app.route('/user/get-user', methods=['POST'])
def get_user():
    pass


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

@app.route('/file/get-info', methods=['POST'])
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
        
        result = fm.get_file_info(paths, keys)
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



@app.route('/file/download', methods=['POST'])
def download():
    pass


@app.route('/file/upload', methods=['POST'])
def upload():
    pass


@app.route('/file/delete', methods=['POST'])
def delete():
    pass


@app.route('/file/create-folder', methods=['POST'])
def create_folder():
    pass


@app.route('/file/rename', methods=['POST'])
def rename():
    pass


@app.route('/file/copy', methods=['POST'])
def copy():
    pass


@app.route('/file/move', methods=['POST'])
def move():
    pass


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


if __name__ == '__main__':
    if cfg.use_ssl:
        app.run(debug=False, host=cfg.host, port=cfg.port, ssl_context=cfg.ssl_context)
    else:
        app.run(debug=False, host=cfg.host, port=cfg.port)