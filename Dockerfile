FROM python:3.8.10-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV RASA_CREDENTIALS=/app/credentials.yml

WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip && \
    pip install rasa && \
    pip install "sqlalchemy<2.0"

# Copy your Rasa project files into the container
# This copies everything from your current directory to /app in the container
COPY . /app

# Train model - only if you haven't trained it and uploaded it
# For production, it's generally better to train locally and upload the model,
# then download it during deployment (as discussed in previous replies).
# If you are training here, ensure your data/ and domain.yml are copied.
RUN rasa train

# Expose the default Rasa port for Docker (Render will still use its own PORT env var)
EXPOSE 5005

# Use the Python script to start Rasa, ensuring the PORT env var is used
CMD ["rasa","run", "--enable-api", "--cors", "*", "--debug"]
