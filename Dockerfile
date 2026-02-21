# Use Python 3.10 as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_huggingface.txt requirements.txt
COPY requirements.txt fallback_requirements.txt

# Install Python dependencies (use lightweight version first, fall back if needed)
RUN pip install --no-cache-dir -r requirements.txt || pip install --no-cache-dir -r fallback_requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p storage/documents storage/temp logs

# Expose port
EXPOSE 7860

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=7860
ENV PYTHONUNBUFFERED=1

# Run database migrations and start application
CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 7860
