FROM python:3.8.10-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5005
ENV RASA_CREDENTIALS=/app/credentials.yml

WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip && \
    pip install rasa sqlalchemy<2.0

COPY . /app

# Train model
RUN rasa train

# Explicitly expose port (critical for Render)
EXPOSE $PORT

# Run Rasa with explicit host binding
CMD exec rasa run \
    --enable-api \
    --cors "*" \
    --port $PORT \
    --credentials $RASA_CREDENTIALS \
    --debug
