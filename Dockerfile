FROM python:3.8.10-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV RASA_CREDENTIALS=/app/credentials.yml

WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip && \
    pip install rasa && \
    pip install "sqlalchemy<2.0" # This is good to prevent the SQLAlchemy 2.0 warning

COPY . /app

# Train model
# Consider training locally and uploading the model to a cloud storage (like Google Cloud Storage
# or AWS S3) and then downloading it during deployment. This makes your build faster.
RUN rasa train

# Explicitly expose port (critical for Render)
EXPOSE 5005

# Run Rasa and bind it to the PORT environment variable provided by Render
# Ensure it binds to 0.0.0.0 so it's accessible externally
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--host", "0.0.0.0", "--port", "${PORT}"]
