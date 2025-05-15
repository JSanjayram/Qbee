# Base image with Python 3.8.10
FROM python:3.8.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY actions/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy custom action code
COPY actions /app

# Expose action server port
EXPOSE 5055

# Run action server
CMD ["rasa", "run", "actions"]
