FROM python:3.9-slim-buster

WORKDIR /app/SlackChannels
COPY ./ /app/SlackChannels/

RUN pip install --upgrade pip && pip install poetry
RUN poetry install

CMD poetry run gunicorn --workers 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080 -m 007 app.main:app --timeout 300