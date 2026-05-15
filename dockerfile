FROM python:3.11-slim

WORKDIR /app

COPY app.py /app/app.py
COPY index.html /app/index.html
WORKDIR /app

RUN pip install flask python-dotenv groq flask-cors

EXPOSE 5000

CMD ["python", "app.py"]

