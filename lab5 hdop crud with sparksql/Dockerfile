FROM python:3.10-slim

WORKDIR /app
COPY . .

# Install Java (required for PySpark)
RUN apt-get update && apt-get install -y \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$PATH:$JAVA_HOME/bin

# Install Python dependencies
RUN pip install pyspark==3.0.0 hdfs

CMD ["python", "app.py"]
