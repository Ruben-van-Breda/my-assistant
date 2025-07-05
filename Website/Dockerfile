# filepath: /Users/rvb/Library/Mobile Documents/com~apple~CloudDocs/Developer/my-assistant/my-assistant/Website/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
COPY src/ /app

# Install required packages
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*  
# Install Flask
# If you have a requirements.txt file, you can copy it and install dependencies from there
# COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# Set environment variables for Flask
ENV FLASK_APP=server.py
ENV FLASK_ENV=development

# Expose the port Flask runs on
EXPOSE 8000

# Run the Flask app use port 8000
# CMD ["flask", "run", "--host=0.0.0.0"]
# pthon3 server.py 
CMD [ "python3", "server.py" ]
# Note: The CMD command runs the Flask application, which will be accessible on port 8000.
# You can change the port number if needed.
# Make sure to adjust the port in your Docker run command if you change it here.
# Example: docker run -p 8000:8000 your_image_name
# This command maps port 8000 of the container to port 8000 on your host
# machine, allowing you to access the Flask app via http://localhost:8000.  