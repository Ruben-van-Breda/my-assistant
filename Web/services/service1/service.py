from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return jsonify(message="Welcome to Service 1!")

@app.route('/health')
def health():
    return jsonify(message="Healthy")

@app.route('/query', methods=['POST', 'OPTIONS'])
def query_post():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
        
    data = request.json
    return jsonify(response=f"You queried: {data['query']}")

@app.route('/create', methods=['POST', 'OPTIONS'])
def create():
    if request.method == 'OPTIONS':
        response = jsonify(success=True)
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        return response
        
    data = request.json
    return jsonify(result=f"Created: {data}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)