FROM python:3.11

RUN apt-get update && apt-get install -y netcat-traditional

WORKDIR /app

COPY pyproject.toml poetry.lock ./

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.7.1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENV PATH="$PATH:$POETRY_HOME/bin"

ARG INSTALL_DEV=false

RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

COPY . .

RUN poetry install

ENTRYPOINT ["sh", "./entrypoint.sh"]