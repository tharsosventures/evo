# Simple Dockerfile for running the evo project on RunPod
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command runs the demo evolution script
CMD ["python", "main.py"]
