FROM python:3.8.10-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5005

WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip && pip install rasa==3.5.11

COPY . /app

# Train model
RUN rasa train

# Explicitly expose port (important for Render)
EXPOSE $PORT

# Run Rasa (using exec form for better signal handling)
CMD exec rasa run --enable-api --cors "*" --port $PORT --debug
