FROM python:3.9-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install

# Copy the rest of the application
COPY . .

# Run the application
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]