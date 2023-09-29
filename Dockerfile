FROM python:3.8-slim-buster

WORKDIR /app

COPY ./app /app

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 8080

ENV NAME World

CMD ["python", "/app/app.py"]