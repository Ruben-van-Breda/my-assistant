# Flask Data Analyser

This project is a basic Flask application that serves an HTML page. It is structured to run on port 5002.

## Project Structure

```
flask-app
├── app.py
├── requirements.txt
├── Dockerfile
├── templates
│   └── index.html
└── README.md
```

## Requirements

To run this application, you need to have Python and Flask installed. You can install the required dependencies using the following command:

```
pip install -r requirements.txt
```

## Running the Application

To run the Flask application, execute the following command:

```
python app.py
```

The application will be accessible at `http://127.0.0.1:5002`.

## Docker

To build and run the application using Docker, follow these steps:

1. Build the Docker image:

   ```
   docker build -t flask-app .
   ```

2. Run the Docker container:

   ```
   docker run -p 5002:5002 flask-app
   ```

The application will be accessible at `http://127.0.0.1:5002` in your web browser.