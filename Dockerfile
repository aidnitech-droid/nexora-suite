FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Set environment PATH to use local pip packages
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Create app user for security
RUN useradd -m -u 1000 nexora && chown -R nexora:nexora /app
USER nexora

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Run with gunicorn (assumes apps.nexora-home.app:app)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "--timeout", "60", "apps.nexora-home.app:app"]
