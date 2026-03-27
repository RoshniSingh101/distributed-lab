# Use a lightweight Python base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies (Flask for API, Requests for node communication)
RUN pip install flask requests flask-cors

# Copy the node logic
COPY app.py .

# Nodes run on port 8000
EXPOSE 8000

# Start the node
CMD ["python", "app.py"]