# ============================================
# Base Stage - Common dependencies
# ============================================
FROM python:3.12-slim AS base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies and security updates
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    curl \
    ca-certificates \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user early
RUN useradd -m -u 1000 appuser \
    && mkdir -p /app/logs \
    && chown -R appuser:appuser /app

# ============================================
# Dependencies Stage - Install Python packages
# ============================================
FROM base AS dependencies

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# ============================================
# Development Stage - For local development
# ============================================
FROM dependencies AS development

# Install development tools
RUN pip install --no-cache-dir \
    pytest \
    pytest-cov \
    black \
    isort \
    flake8 \
    mypy

# Copy application code
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run with hot reload
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ============================================
# Production Stage - Optimized for production
# ============================================
FROM dependencies AS production

# Copy application code
COPY --chown=appuser:appuser . .

# Make entrypoint executable
RUN chmod +x docker-entrypoint.sh

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/docs || exit 1

# Expose port
EXPOSE 8000

# Use entrypoint script for initialization
ENTRYPOINT ["./docker-entrypoint.sh"]

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
