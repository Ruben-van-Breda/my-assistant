from flask import Flask, render_template
import requests
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create')
def create():
    try:
        response = requests.post('http://service1:5000/', json={'name': 'John'})
        return render_template('create.html', response=response.json())
    except Exception as e:
        return render_template('create.html', response=f"Error: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)