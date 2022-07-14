FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /srv
COPY ./pyproject.toml ./poetry.lock ./
RUN pip3 install poetry
RUN poetry install
