FROM python:3.11-slim

WORKDIR /app

COPY index.html .

RUN pip install flask python-dotenv groq flask-cors

EXPOSE 5000

CMD ["python", "app.py"]