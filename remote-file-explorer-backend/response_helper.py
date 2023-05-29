from flask import jsonify


def pack_response(success, message, data=None):
    response_data = {
        'success': success,
        'message': message,
        'data': data
    }
    return jsonify(response_data)