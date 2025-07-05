# Use official Python image
FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Install dependencies if requirements.txt exists
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

EXPOSE 8080

CMD ["python", "app.py"]
