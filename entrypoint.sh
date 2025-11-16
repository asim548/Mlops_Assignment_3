#!/bin/bash
set -e

echo "Starting Airflow initialization..."

# Initialize the database
echo "Initializing Airflow database..."
airflow db migrate 2>&1 || echo "Database migration in progress..."

# Create default connections
echo "Creating default connections..."
airflow connections create-default-connections 2>&1 || true

# Create admin user
echo "Creating admin user..."
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com 2>&1 || echo "Admin user already exists"

echo "Airflow initialization complete!"
echo "Starting webserver and scheduler..."

# Start webserver in background
airflow webserver -p 8080 &
WEBSERVER_PID=$!

# Start scheduler in foreground
exec airflow scheduler
