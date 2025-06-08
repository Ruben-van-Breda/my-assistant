from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Flask Web App!"})

@app.route('/health')
def health_check():
    return "Service is running!"

@app.route('/help')
def help_page():
    return "This is the help page for the Flask Web App."

# Example API endpoint for processing data
@app.route('/process', methods=['POST'])
def process_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Example processing logic
    processed_data = {key: value.upper() for key, value in data.items()}
    return jsonify({"processed_data": processed_data})

# Example API endpoint for querying
@app.route('/query', methods=['GET'])
def query_data():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Example query logic
    response = {"query": query, "result": f"Processed result for '{query}'"}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)