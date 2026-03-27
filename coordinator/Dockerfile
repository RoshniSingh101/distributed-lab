# Use a lightweight Python base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies (Flask for API, Requests for node communication)
RUN pip install flask requests flask-cors

# Copy all modular components
COPY app.py .
COPY strategies.py .
COPY monitor.py .

# Coordinator runs on port 5000
EXPOSE 5000

# Start the brain
CMD ["python", "app.py"]