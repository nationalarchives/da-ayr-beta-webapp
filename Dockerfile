# Build stage for Node.js assets
FROM node:24-slim AS node-builder

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY app/static/src app/static/src

RUN npm run build

# Base Python stage
FROM python:3.11-slim AS python-base

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    openssl \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false

RUN poetry install --no-root

# Copy CSS from build stage
COPY --from=node-builder /app/app/static/src/css app/static/src/css

RUN openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 \
    -subj "/C=GB/ST=England/L=London/O=Test/CN=DNS:localhost,IP:127.0.0.1"

EXPOSE 5000

# Development stage - for hot reloading
FROM python-base AS development

# In development, source code will be mounted as volume
# so we don't need to COPY it here for dev builds
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VENV_IN_PROJECT=false
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

# Ensure Poetry doesn't try to use any .venv from mounted source
RUN poetry config virtualenvs.create false
RUN poetry config virtualenvs.in-project false

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]

# Production stage - for CI/production builds
FROM python-base AS production

COPY . .

CMD ["poetry", "run", "python", "-m", "flask", "--app", "main_app:app", "run", "--host=0.0.0.0", "--port=5000"]
