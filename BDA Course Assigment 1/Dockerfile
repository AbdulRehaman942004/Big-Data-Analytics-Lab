# Use Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy the main.py file
COPY main.py .

# Create storage directory
RUN mkdir -p hdfs_storage

# Run the application
CMD ["python", "main.py"]
