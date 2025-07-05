from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify(message="Welcome to Service 1!")

@app.route('/hello')
def hello():
    return jsonify(message="Hello World!")

@app.route('/query')
def query():
    q = request.args.get('q', '')
    return jsonify(result=f"You queried: {q}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)