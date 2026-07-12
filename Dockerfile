# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for VTK and other packages
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libosmesa6 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Upgrade pip, then install Python dependencies
# --prefer-binary: never compile from source (required on ARM64 where some wheels are missing)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy application code
COPY . .

# Expose port (Coolify will handle the actual port mapping)
EXPOSE 3000

# Run the application
CMD ["python", "main.py"]
