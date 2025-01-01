FROM python:3.9-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry install

COPY . .

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]