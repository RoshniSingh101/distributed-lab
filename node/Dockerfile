# Use a lightweight Python base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install flask

# Copy the node logic
COPY app.py .

# Nodes run on port 8000
EXPOSE 8000

# Start the node
CMD ["python", "app.py"]