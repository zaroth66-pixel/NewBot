FROM python:3.12-slim

############################
# Environment
############################
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

############################
# Working directory
############################
WORKDIR /app

############################
# System packages
############################
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    curl \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

############################
# Upgrade pip
############################
RUN pip install --upgrade pip setuptools wheel

############################
# Install dependencies
############################
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

############################
# Copy source
############################
COPY . .

############################
# Create user
############################
RUN useradd --create-home --shell /bin/bash botuser && \
    chown -R botuser:botuser /app

USER botuser

############################
# Port
############################
EXPOSE 8000

############################
# Health Check
############################
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
CMD curl -f http://localhost:8000/health || exit 1

############################
# Start
############################
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
