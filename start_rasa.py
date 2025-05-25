import os
import subprocess
import sys

# Get the port from the environment variable (Render provides this)
port = os.environ.get('PORT', '5005') # Default to 5005 if PORT is not set (good for local testing)

# Get the host from the environment variable (Render might not provide this, but good practice)
host = os.environ.get('HOST', '0.0.0.0')

# Construct the Rasa command
# Using a list for subprocess.run for safer argument handling
command = [
    "rasa",
    "run",
    "--enable-api",
    "--cors", "*",
    "--host", host,
    "--port", port
]

print(f"Starting Rasa server with command: {' '.join(command)}")

# Execute the Rasa command
try:
    # Use subprocess.run to execute the command
    # check=True will raise an exception if the command exits with a non-zero status
    # This helps in debugging if Rasa itself fails to start
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    print(f"Error starting Rasa server: {e}", file=sys.stderr)
    sys.exit(1) # Exit with an error code if Rasa fails to start
except Exception as e:
    print(f"An unexpected error occurred: {e}", file=sys.stderr)
    sys.exit(1)
