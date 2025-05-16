#!/bin/sh

PORT_TO_USE=${PORT:-5005}
echo "Starting Rasa on port $PORT_TO_USE"

rasa run \
  --enable-api \
  --cors "*" \
  --debug \
  --port "$PORT_TO_USE" \
  --host "0.0.0.0"
