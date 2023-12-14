FROM python:3.9-slim-bullseye

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 32168

CMD ["python", "app.py"]
