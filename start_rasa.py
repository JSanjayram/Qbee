import os
import subprocess
import sys

# Get the port from the environment variable (Render provides this)
port = os.environ.get('PORT', '5005') # Default to 5005 if PORT is not set (good for local testing)

# Construct the Rasa command WITHOUT --host
command = [
    "rasa",
    "run",
    "--enable-api",
    "--cors", "*",
    "--port", port
]

print(f"Starting Rasa server with command: {' '.join(command)}")

# Execute the Rasa command
try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error starting Rasa server: {e}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred: {e}", file=sys.stderr)
    sys.exit(1)
