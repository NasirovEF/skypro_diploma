FROM python:3.10

WORKDIR /homework

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

