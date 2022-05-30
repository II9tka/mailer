FROM python:3.9-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && upgrade -y && apt-get -y install postgresql gcc python3-dev musl-dev

RUN python3 -m pip install --upgrade pip
RUN pip install --no-cache-dir poetry

COPY pyproject.toml /app/
COPY poetry.lock /app/

RUN poetry config virtualenvs.create false

RUN poetry install

COPY . /app