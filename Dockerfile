FROM python:3.12-slim

WORKDIR /app

# Install system dependencies needed for XGBoost multi-core operations
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Ingest dependencies first to leverage Docker cache layers
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the cleaned application codebase
COPY . .

EXPOSE 8080
EXPOSE 9501
