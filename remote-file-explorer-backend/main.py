from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/data')
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

if __name__ == '__main__':
    if __name__ == '__main__':
        app.run(debug=False)