# Stage 1: Build the requirements.txt using Poetry
FROM python:3.12-slim AS builder

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only the poetry.lock/pyproject.toml to leverage Docker cache
WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# Install dependencies and create requirements.txt
RUN poetry export --format=requirements.txt --output=requirements.txt --only=main

# Stage 2: Install dependencies and run the Django application
FROM python:3.12-slim AS runner

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the generated requirements.txt from the builder stage
WORKDIR /app
COPY --from=builder /app/requirements.txt /app/

# Install application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Run the Django application with Gunicorn
EXPOSE 8000
CMD ["gunicorn", "--workers=9", "--bind=0.0.0.0:8000", "panso.wsgi:application", "--log-level=info", "--access-logfile=-", "--error-logfile=-"]
