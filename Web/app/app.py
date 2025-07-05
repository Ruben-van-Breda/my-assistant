from flask import Flask, render_template, request, jsonify, send_from_directory, session
import requests
import os
import json

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Create output directory if it doesn't exist
HTML_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'generated')
os.makedirs(HTML_OUTPUT_DIR, exist_ok=True)

# Load services configuration
def load_services_config():
    global services_config
    print("Loading services config")
    config_path = os.path.join(os.path.dirname(__file__), 'services.config.json')
    with open(config_path, 'r') as f:
        services_config = json.load(f)
    print("Services config loaded")
    print(services_config)
    return services_config

@app.route('/')
def index():
    # Auth
    authenticate()
    # request services config
    config = load_services_config()

    # load user files   
    user_files = load_user_files()
    return render_template('index.html', config=config, user_files=user_files) 

def authenticate():
    # set session cookie
    session['user_id'] = '123'
    print("Session cookie set")
    print(session)
    return True

@app.route('/create')
def create():
    try:
        # Ensure user is authenticated
        if not authenticate():
            return render_template('create.html', config={}, user_files=[], error="Authentication failed")

        # Request services config
        try:
            config = load_services_config()
        except Exception as e:
            print(f"Error loading services config: {e}")
            config = {}

        # Load user files - already handles errors internally
        user_files = load_user_files()

        return render_template('create.html', config=config, user_files=user_files)
    except Exception as e:
        print(f"Error in create route: {e}")
        return render_template('create.html', config={}, user_files=[], error=str(e))

@app.route('/services_config')
def get_services_config():
    try:
        config = load_services_config()
        return jsonify(config)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def load_user_files():
    try:
        print("Loading user files")
        user_id = session.get("user_id")
        if not user_id:
            print("No user_id in session")
            return []

        # Ensure output directory exists
        if not os.path.exists(HTML_OUTPUT_DIR):
            print("Output directory does not exist")
            os.makedirs(HTML_OUTPUT_DIR, exist_ok=True)
            return []

        # Load and filter files
        try:
            files = os.listdir(HTML_OUTPUT_DIR)
            files = [file for file in files if file.startswith(user_id)]
            print("User files loaded:", files)
            return files
        except Exception as e:
            print(f"Error listing files: {e}")
            return []

    except Exception as e:
        print(f"Error in load_user_files: {e}")
        return []

@app.route('/save_html', methods=['POST'])
def save_html():
    try:
        data = request.get_json()
        html_content = data.get('html')
        if not html_content:
            return jsonify({'error': 'No HTML content provided'}), 400
            
        # Save HTML to a file
        filename = f'{session["user_id"]}_generated_app.html'
        filepath = os.path.join(HTML_OUTPUT_DIR, filename)
        with open(filepath, 'w') as f:
            f.write(html_content)
            
        # Return the URL where the file can be accessed
        return jsonify({
            'message': 'HTML saved successfully',
            'url': f'/static/generated/{filename}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)