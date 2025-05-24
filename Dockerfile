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

COPY . /app

# Train model
RUN rasa train

# Explicitly expose port (critical for Render)
EXPOSE 5005


# Run Rasa with explicit host binding
CMD ["sh", "-c", "rasa run --enable-api --cors '*' --port ${PORT}"]

