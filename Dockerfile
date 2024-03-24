FROM python:3.11

WORKDIR /app

COPY pyproject.toml poetry.lock ./

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.7.1
ENV PATH="$PATH:$POETRY_HOME/bin"

ARG INSTALL_DEV=false

# Установка инструмента poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VERSION

# Копирование остальных файлов
COPY . .

# Установка зависимостей с помощью poetry
RUN poetry install --no-dev

ENTRYPOINT ["sh", "./entrypoint.sh"]
