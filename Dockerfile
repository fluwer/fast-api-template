FROM python:3.12.0-slim

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    openssh-client \
    autossh \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on
ENV POETRY_VERSION=1.8.5
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH=/backend/src

RUN mkdir /backend
WORKDIR /backend

COPY pyproject.toml poetry.lock /backend/
RUN python -m pip install --upgrade pip
RUN pip install --upgrade pip setuptools
RUN pip install poetry==${POETRY_VERSION}
RUN poetry install --no-ansi

COPY . .