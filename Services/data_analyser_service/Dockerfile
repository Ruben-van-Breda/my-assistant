# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Make port 5002 available to the world outside this container
EXPOSE 3001

# Run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port=3001", "--server.address=0.0.0.0"]
