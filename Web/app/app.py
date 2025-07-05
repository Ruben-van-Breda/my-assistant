from flask import Flask, render_template, request, jsonify, send_from_directory, session
import requests
import os
import json
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Create output directory if it doesn't exist
HTML_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'static', 'generated')
os.makedirs(HTML_OUTPUT_DIR, exist_ok=True)

# Create projects directory in static
PROJECTS_DIR = os.path.join(os.path.dirname(__file__), 'static', 'projects')
os.makedirs(PROJECTS_DIR, exist_ok=True)

# Project root directory (parent of app directory)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
APP_ROOT = os.path.dirname(__file__)

def get_user_project_dir():
    """Get or create user's project directory."""
    user_id = session.get('user_id', 'default')
    user_project_dir = os.path.join(PROJECTS_DIR, user_id)
    
    # Create user project directory if it doesn't exist
    if not os.path.exists(user_project_dir):
        os.makedirs(user_project_dir, exist_ok=True)
        
        # Copy template files from app directory
        try:
            # Copy templates
            templates_src = os.path.join(APP_ROOT, 'templates')
            templates_dst = os.path.join(user_project_dir, 'templates')
            if os.path.exists(templates_src) and not os.path.exists(templates_dst):
                shutil.copytree(templates_src, templates_dst)

            # Copy static files (excluding projects directory)
            static_src = os.path.join(APP_ROOT, 'static')
            static_dst = os.path.join(user_project_dir, 'static')
            if os.path.exists(static_src) and not os.path.exists(static_dst):
                os.makedirs(static_dst)
                # Copy specific static directories/files, excluding 'projects'
                for item in os.listdir(static_src):
                    if item != 'projects':
                        src_item = os.path.join(static_src, item)
                        dst_item = os.path.join(static_dst, item)
                        if os.path.isdir(src_item):
                            shutil.copytree(src_item, dst_item)
                        else:
                            shutil.copy2(src_item, dst_item)

            print(f"Project files copied for user {user_id}")
        except Exception as e:
            print(f"Error copying project files: {e}")
    
    return user_project_dir

def get_project_files():
    """Get list of project files from user's project directory."""
    try:
        user_project_dir = get_user_project_dir()
        project_files = []
        
        for root, dirs, files in os.walk(user_project_dir):
            # Skip hidden directories and files
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['venv', '__pycache__', 'node_modules']]
            files = [f for f in files if not f.startswith('.')]
            
            for file in files:
                # Get relative path from user's project directory
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, user_project_dir)
                
                # Skip binary and large files
                try:
                    if os.path.getsize(full_path) < 1024 * 1024:  # Skip files larger than 1MB
                        # Determine file type based on extension
                        _, ext = os.path.splitext(file)
                        file_type = 'file'
                        if ext in ['.html', '.htm']:
                            file_type = 'html'
                        elif ext in ['.py', '.js', '.ts', '.jsx', '.tsx']:
                            file_type = 'code'
                        elif ext in ['.css', '.scss', '.sass']:
                            file_type = 'style'
                        elif ext in ['.json', '.yaml', '.yml']:
                            file_type = 'data'
                        
                        project_files.append({
                            'path': rel_path,
                            'name': file,
                            'type': file_type,
                            'directory': os.path.dirname(rel_path)
                        })
                except OSError:
                    continue  # Skip files that can't be accessed
        
        # Sort files by directory and name
        project_files.sort(key=lambda x: (x['directory'], x['name']))
        return project_files
    except Exception as e:
        print(f"Error getting project files: {e}")
        return []

# Load services configuration
def load_services_config():
    global services_config
    print("Loading services config")
    try:
        config_path = os.path.join(os.path.dirname(__file__), 'services.config.json')
        print(f"Config path: {config_path}")
        with open(config_path, 'r') as f:
            services_config = json.load(f)
        print("Services config loaded successfully")
        print(f"Config: {services_config}")
        return services_config
    except Exception as e:
        print(f"Error loading services config: {e}")
        return {"services": [], "environment": "development"}

@app.route('/')
def index():
    # Auth
    authenticate()
    # request services config
    config = load_services_config()
    # Initialize user's project directory
    get_user_project_dir()
    # load user files   
    user_files = load_user_files()
    project_files = get_project_files()
    return render_template('index.html', config=config, user_files=user_files, project_files=project_files)

def authenticate():
    # set session cookie
    if 'user_id' not in session:
        session['user_id'] = '123'
        # Initialize user's project directory on first login
        get_user_project_dir()
    print("Session cookie set")
    print(session)
    return True

@app.route('/create')
def create():
    print("Creating new project")
    try:
        # Ensure user is authenticated
        if not authenticate():
            return render_template('create.html', config={}, user_files=[], project_files=[], error="Authentication failed")

        # Request services config
        try:
            config = load_services_config()
        except Exception as e:
            print(f"Error loading services config: {e}")
            config = {}

        # Load user files - already handles errors internally
        user_files = load_user_files()
        project_files = get_project_files()

        return render_template('create.html', config=config, user_files=user_files, project_files=project_files)
    except Exception as e:
        print(f"Error in create route: {e}")
        return render_template('create.html', config={}, user_files=[], project_files=[], error=str(e))

@app.route('/get_file_content', methods=['GET'])
def get_file_content():
    try:
        file_path = request.args.get('path')
        if not file_path:
            return jsonify({'error': 'No file path provided'}), 400

        # Get content from user's project directory
        user_project_dir = get_user_project_dir()
        full_path = os.path.join(user_project_dir, file_path)
        
        # Ensure the path is within the user's project directory
        if not os.path.commonpath([full_path, user_project_dir]) == user_project_dir:
            return jsonify({'error': 'Invalid file path'}), 403

        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            return jsonify({'error': 'File not found'}), 404

        # Read and return file content
        with open(full_path, 'r') as f:
            content = f.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save_project_file', methods=['POST'])
def save_project_file():
    try:
        data = request.get_json()
        file_path = data.get('path')
        content = data.get('content')
        
        if not file_path or content is None:
            return jsonify({'error': 'Missing file path or content'}), 400
            
        # Save to user's project directory
        user_project_dir = get_user_project_dir()
        full_path = os.path.join(user_project_dir, file_path)
        
        # Ensure the path is within the user's project directory
        if not os.path.commonpath([full_path, user_project_dir]) == user_project_dir:
            return jsonify({'error': 'Invalid file path'}), 403
            
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
        # Save the file
        with open(full_path, 'w') as f:
            f.write(content)
            
        return jsonify({
            'message': 'File saved successfully',
            'path': file_path
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

        # Get user's directory in static/projects
        user_dir = os.path.join(PROJECTS_DIR, user_id)
        
        # Ensure directory exists
        if not os.path.exists(user_dir):
            print("User directory does not exist")
            os.makedirs(user_dir, exist_ok=True)
            return []

        # Load and filter files
        try:
            files = [f for f in os.listdir(user_dir) if f.endswith('.html')]
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
        should_save = data.get('save', False)
        filename = data.get('filename', 'generated_app.html')
        
        if not html_content:
            return jsonify({'error': 'No HTML content provided'}), 400
            
        # Get user's project directory
        user_id = session.get('user_id', 'default')
        
        # Save directly to static/projects/{userid}/
        user_dir = os.path.join(PROJECTS_DIR, user_id)
        
        # Ensure user directory exists
        os.makedirs(user_dir, exist_ok=True)
            
        # Clean filename and ensure it ends with .html
        safe_filename = secure_filename(filename)
        if not safe_filename.endswith('.html'):
            safe_filename += '.html'
            
        filepath = os.path.join(user_dir, safe_filename)
        
        if should_save:
            # Save to permanent location if save is requested
            with open(filepath, 'w') as f:
                f.write(html_content)
            
        # Return the URL where the file can be accessed
        return jsonify({
            'message': 'HTML saved successfully' if should_save else 'HTML generated successfully',
            'url': f'/static/projects/{user_id}/{safe_filename}',
            'saved': should_save,
            'filename': safe_filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_file', methods=['POST'])
def delete_file():
    try:
        data = request.get_json()
        filename = data.get('filename')
        
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400
            
        # Get user's directory
        user_id = session.get('user_id', 'default')
        user_dir = os.path.join(PROJECTS_DIR, user_id)
        
        # Construct full file path
        filepath = os.path.join(user_dir, secure_filename(filename))
        
        # Ensure the path is within the user's directory
        if not os.path.commonpath([filepath, user_dir]) == user_dir:
            return jsonify({'error': 'Invalid file path'}), 403
            
        # Check if file exists
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
            
        # Delete the file
        os.remove(filepath)
        
        return jsonify({
            'message': 'File deleted successfully',
            'filename': filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)