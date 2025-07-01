import os
from flask import Flask, request
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)

