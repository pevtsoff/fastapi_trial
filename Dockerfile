FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

WORKDIR /srv
COPY ./pyproject.toml ./poetry.lock ./

RUN pip3 install poetry
RUN poetry export -f requirements.txt --output requirements.txt
RUN poetry install

RUN pip install -r requirements.txt # this is for debugging via pycharm, so in prod can be omitted
