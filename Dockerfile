FROM python:3.11-slim

# Install build tools and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc libffi-dev libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port 5000 to make it accessible
EXPOSE 5000

# Run app with auto-instrumentation
CMD ["opentelemetry-instrument", "python3", "app.py"]
