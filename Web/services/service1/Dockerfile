# Use official Python image
FROM python:3.10-slim

WORKDIR /service1

COPY . /service1

# Install dependencies if requirements.txt exists
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

EXPOSE 5001

CMD ["python", "service.py"]
