# Use Python 3.8.10 as base
FROM python:3.8.10-slim

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install Rasa Open Source
RUN pip install --upgrade pip && pip install rasa==3.5.11

# Copy files
COPY . /app

# Expose Rasa port
EXPOSE 5005

# Run Rasa server
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug"]
