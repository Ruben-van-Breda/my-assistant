from flask import Flask, request, jsonify
from flask_cors import CORS

import openai


import os
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes



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


def read_file(filename):
    with open(filename, "r") as f:
        return f.read()
    return ""

# Send a prompt to ChatGPT
def Query(prompt, model="gpt-4"):
    system_prompt = ""
    try:
        # read the file
        system_prompt = read_file("system_prompt.txt")
        print(system_prompt)

    except Exception as e:
        print(f"❌ Error: {e}")


        
    response = openai.chat.completions.create(
        model=model,
        messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
    )    

        # valid_html = openai.chat.completions.create(
        #     model=model,
        #     messages=[
        #         {"role": "system", "content": "Improve and ensure code works. \n" + system_prompt},
        #         {"role": "user", "content": response.choices[0].message.content}
        #     ],
        #     temperature=0.1,
        # )
        # return valid_html.choices[0].message.content


      
        
    return response.choices[0].message.content
    

    
SetupAgent()

@app.route('/')
def home():
    # set window title
  


    return jsonify({"message": "HTML Service is running!"})

    return response

@app.route('/health')
def health_check():
    return "Service is running!"

@app.route('/help')
def help_page():
    return "This is HTML Service, providing various endpoints for data processing and querying."

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
    chat_response = Query(query)
    # Here you would typically call the OpenAI API or another service to process the query

    return jsonify({"query": query, "response": chat_response})

@app.route('/query', methods=['POST'])
def chat():
    data = request.get_json()
    print(data)
    if not data or 'query' not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data['query']
    chat_response = Query(user_message)
    return jsonify({"response": chat_response})

@app.route('/save_html', methods=['POST'])
def save_html():
    data = request.get_json()
    print(data)
    return jsonify({"message": "HTML saved!"})


if __name__ == '__main__':
    app.run(debug=True, port=3001, host='0.0.0.0')
