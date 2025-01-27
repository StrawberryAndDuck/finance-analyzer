FROM python:3.10-slim

ARG DEBIAN_FRONTEND=noninteractive
RUN pip install --upgrade pip && pip install poetry
WORKDIR /app

COPY pyproject.toml /app/
COPY poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry install

COPY ./ /app/
CMD ["sh", "-c", "/app/scripts/run.sh"]
