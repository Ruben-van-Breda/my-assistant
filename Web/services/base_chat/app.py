from flask import Flask, request, jsonify
from flask_cors import CORS

import openai
import os

app = Flask(__name__)
# Configure CORS to allow requests from your frontend
CORS(app)



# Setup the OpenAI client
def SetupAgent():
    # api_key_path = "/run/secrets/openai_api_key"
    api_key_path = "./secrets.txt"  # Adjust the path as needed
    if not os.path.exists(api_key_path):
        raise FileNotFoundError(f"❌ API key file not found at {api_key_path}.")
    
    with open(api_key_path, "r") as f:
        api_key = f.read().strip()
    
    if not api_key:
        raise ValueError("❌ API key is empty.")
    
    openai.api_key = api_key

    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = api_key

    print("✅ OpenAI Agent setup complete.")


# Send a prompt to ChatGPT
def QueryText(prompt, model="gpt-4"):
    try:
        system_prompt = "You are a helpful assistant."
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"

def QueryImage(prompt, size="1024x1024"):
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            response_format="b64_json"   # request base64 output
        )
        
        # Extract base64 string
        image_base64 = response.data[0].b64_json
        return image_base64
    except Exception as e:
        return f"❌ Error: {e}"

# Example usage:
    
SetupAgent()

@app.route('/')
def home():
    return jsonify({"message": "ChatGPT Service is running!"})


@app.route('/health')
def health_check():
    return "Service is running!"

@app.route('/help')
def help_page():
    return "This is ChatGPT Service, providing various endpoints for data processing and querying."

@app.route('/image', methods=['GET', 'POST'])
def handle_image():
    # Get prompt from either query parameters or JSON body
    if request.method == 'GET':
        prompt = request.args.get('prompt')
    else:  # POST
        data = request.get_json()
        prompt = data.get('prompt') if data else None
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    try:
        image_base64 = QueryImage(prompt)
        return jsonify({"image": image_base64})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
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
# @app.route('/query', methods=['GET'])
# def query_data():
#     query = request.args.get('q', '')
#     if not query:
#         return jsonify({"error": "No query provided"}), 400

#     # Example query logic
#     chat_response = Query(query)
#     # Here you would typically call the OpenAI API or another service to process the query

#     return jsonify({"query": query, "response": chat_response})

@app.route('/query', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data['query']
    if 'image' in user_message:
        try:
            image_base64 = QueryImage(user_message)
            return jsonify({"image": image_base64})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        try:
            chat_response = QueryText(user_message)
            return jsonify({"response": chat_response})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0')
