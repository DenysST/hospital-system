# Use Python 3.12 slim as base image
FROM python:3.12-slim

# Set environment variables for Flask
ENV FLASK_APP=app.py \
    FLASK_ENV=development \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Copy project files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root

# Copy the rest of the application code
COPY . .

# Expose the default Flask port
EXPOSE 5000

# Command to run the application
CMD ["poetry", "run", "python", "setup.py", "--start-app"]
