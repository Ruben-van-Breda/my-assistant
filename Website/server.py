import os
from flask import Flask, jsonify, request, send_from_directory
import site as site
from flask_cors import CORS


port = os.environ.get('PORT', 8080)
app = Flask(__name__, static_folder="src", static_url_path="")
CORS(app)  # Enable CORS for all routes

@app.route("/")
def root():
    return app.send_static_file("index.html")

@app.route("/health")
def health():
    print("Health check endpoint hit")
    # This endpoint can be used to check if the server is running
    return "OK", 200


@app.route("/create_app", methods=["GET","POST"])
def create_app_view():
    if request.method == "GET":
        return app.send_static_file("./create_application/agent_chat.html")
    elif request.method == "POST":
        print("Chat POST endpoint hit")
        # Here you would handle the chat request, e.g., process user input
        return "Chat functionality is not implemented yet", 501

@app.route("/view", methods=["GET"])
def view_app():
    print("View app endpoint hit")
    # Serve output.html from html_output directory
    output_dir = os.path.join(os.getcwd(), "html_output")
    return send_from_directory(output_dir, "output.html")

@app.route('/save', methods=['POST', 'OPTIONS'])
def save_html():
    print("Save HTML endpoint hit")  # Debugging line
    if request.method == 'OPTIONS':
        # CORS preflight response
        return '', 204
    data = request.get_json()
    html = data.get('html')
    filename = data.get('filename', 'output.html')

    if not html:
        return jsonify({"error": "No HTML content provided"}), 400

    try:
        # Save to html_output directory
        output_dir = os.path.join(os.getcwd(), "html_output")
        print(f"Output directory: {output_dir}")  # Debug
        print(f"Filename: {filename}")            # Debug
        print(f"HTML: {html[:100]}")              # Debug (prints first 100 chars)

        os.makedirs(output_dir, exist_ok=True)

        filepath = os.path.join(output_dir, filename)
        print(f"Full file path: {filepath}")       # Debug

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)

        return jsonify({"message": f"✅ HTML saved as {filename}", "path": filepath})
    except Exception as e:
        print(f"Error saving HTML: {e}")  # Add this line for debugging
        return jsonify({"error": str(e)}), 500
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

