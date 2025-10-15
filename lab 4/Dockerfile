# Use Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Ensure storage directory exists
RUN mkdir -p hdfs_storage

# Run the application
CMD ["python", "main.py"]
