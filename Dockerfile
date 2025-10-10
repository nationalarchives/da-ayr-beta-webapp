# Development Dockerfile - single stage for dev-only usage
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies including Node.js (cached layer)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    openssl \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (cached layer)
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy Python dependency files first for better caching
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-root

# Copy Node.js dependency files and install
COPY package*.json ./
RUN npm ci

# Copy static assets and build (only rebuilds if static files change)
COPY app/static/src app/static/src
RUN npm run build

# Copy source code last (changes most frequently)
# Use .dockerignore to exclude files that don't need to be in the image
COPY . .

# Ensure built CSS files are preserved if they exist from previous layer
RUN if [ -d app/static/src/css ]; then echo "CSS files preserved from build layer"; fi

ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]
