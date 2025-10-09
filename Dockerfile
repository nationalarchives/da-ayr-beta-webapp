# Development Dockerfile - single stage for dev-only usage
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies including Node.js
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    openssl \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy and install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

# Copy and build Node.js assets
COPY package*.json ./
RUN npm ci

COPY app/static/src app/static/src
RUN npm run build

# Copy source code for development
COPY . .

# Create SSL certificates for development
RUN openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 \
    -subj "/C=GB/ST=England/L=London/O=Test/CN=DNS:localhost,IP:127.0.0.1"

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]
