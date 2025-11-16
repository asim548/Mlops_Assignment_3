FROM apache/airflow:2.9.1-python3.10

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ssh \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy and install Python requirements
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Initialize DVC
RUN dvc init --no-scm 2>/dev/null || true

# Copy airflow configuration
COPY airflow /opt/airflow
WORKDIR /opt/airflow

# Create necessary directories
RUN mkdir -p /opt/airflow/data/raw /opt/airflow/data/processed

EXPOSE 8080

CMD ["bash"]

