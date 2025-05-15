FROM python:3.8.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 5055
CMD ["python", "-m", "rasa_sdk", "--actions", "actions", "--port", "5055"]
