# Simple HTML Server

This project sets up a simple HTTP server to serve an HTML page.

## Project Structure
```
simple-html-server
├── src
│   └── index.html        # HTML content served by the server
├── server.py             # Main entry point for the HTTP server
├── requirements.txt      # Dependencies required for the project
├── Dockerfile            # Instructions to build a Docker image
└── README.md             # Documentation for the project
```

## Getting Started

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   cd simple-html-server
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Server
To start the server, run the following command:
```
python server.py
```
The server will be running at `http://localhost:8000`.

### Docker
To build and run the Docker container, use the following commands:
1. Build the Docker image:
   ```
   docker build -t simple-html-server .
   ```

2. Run the Docker container:
   ```
   docker run -d -p 8000:8000 simple-html-server
   ```

### Accessing the Web Page
Open your web browser and navigate to `http://localhost:8000` to view the HTML page served by the server.

## License
This project is licensed under the MIT License - see the LICENSE file for details.