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

RUN chmod +x /app/entrypoint.sh


RUN rasa train

# Expose Rasa port
EXPOSE 5005

# Run Rasa server
#CMD ["sh", "-c", "rasa run --enable-api --cors '*' --debug --port ${PORT:-5005} --host 0.0.0.0"]
#CMD ["/app/entrypoint.sh"]
#CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005", "--debug"]
#CMD ["rasa", "run", "--enable-api", "--cors", "*", "--port", "5005", "--host", "0.0.0.0", "--debug"]
CMD rasa run --enable-api 
