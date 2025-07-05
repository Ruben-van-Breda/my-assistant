import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

port = int(os.environ.get('PORT', 8000))
app = Flask(__name__, static_folder="src", static_url_path="")
CORS(app)

@app.route("/")
def root():
    return app.send_static_file("index.html")

@app.route("/health")
def health():
    print("Health check endpoint hit")
    return "OK", 200

@app.route("/create_app", methods=["GET", "POST"])
def create_app_view():
    if request.method == "GET":
        return send_from_directory(
            os.path.join(app.static_folder, "create_application"),
            "agent_chat.html"
        )
    elif request.method == "POST":
        print("Chat POST endpoint hit")
        return "Chat functionality is not implemented yet", 501

@app.route("/view", methods=["GET"])
def view_app():
    print("View app endpoint hit")
    output_dir = os.path.join(os.getcwd(), "html_output")
    return send_from_directory(output_dir, "output.html")

@app.route('/save', methods=['POST', 'OPTIONS'])
def save_html():
    print("Save HTML endpoint hit")
    if request.method == 'OPTIONS':
        return '', 204
    data = request.get_json()
    html = data.get('html')
    filename = data.get('filename', 'output.html')
    if not html:
        return jsonify({"error": "No HTML content provided"}), 400
    try:
        output_dir = os.path.join(os.getcwd(), "html_output")
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        return jsonify({"message": f"✅ HTML saved as {filename}", "path": filepath})
    except Exception as e:
        print(f"Error saving HTML: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

