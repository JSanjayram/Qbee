#!/bin/sh
# entrypoint.sh

# Use Render's $PORT if available, otherwise default to 5005
PORT_TO_USE=${PORT:-5005}

echo "Starting Rasa server on port $PORT_TO_USE..."
rasa run --enable-api --cors '*' --debug --port "$PORT_TO_USE" --host 0.0.0.0
