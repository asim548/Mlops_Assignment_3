#!/bin/bash
# MLOps APOD Pipeline - Quick Start Script for Linux/Mac
# This script sets up and starts the complete pipeline

set -e

echo ""
echo "================================================"
echo "  MLOps APOD ETL Pipeline - Quick Start"
echo "================================================"
echo ""

# Check if Docker is installed
echo "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed"
    echo "Please install Docker Desktop from https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "Docker found:"
docker --version
echo ""

# Check if Git is installed
echo "Checking Git installation..."
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed"
    echo "Please install Git from https://git-scm.com/"
    exit 1
fi

echo "Git found:"
git --version
echo ""

# Set environment variables
echo "Setting environment variables..."
export NASA_API_KEY="DEMO_KEY"

# Build Docker image
echo ""
echo "Building Docker image (this may take 5-10 minutes)..."
docker-compose build --no-cache

if [ $? -ne 0 ]; then
    echo "ERROR: Docker build failed"
    exit 1
fi

echo "Docker build completed successfully!"
echo ""

# Start services
echo "Starting services (Postgres + Airflow)..."
docker-compose up -d

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to start services"
    exit 1
fi

echo ""
echo "================================================"
echo "  ✓ Services started!"
echo "================================================"
echo ""
echo "Waiting for services to be ready (30 seconds)..."
sleep 30

echo ""
echo "================================================"
echo "  Airflow Setup Complete!"
echo "================================================"
echo ""
echo "Access Airflow UI:"
echo "  URL: http://localhost:8080"
echo "  Username: admin"
echo "  Password: admin"
echo ""
echo "PostgreSQL:"
echo "  Host: localhost"
echo "  Port: 5432"
echo "  User: airflow"
echo "  Password: airflow"
echo ""
echo "Next steps:"
echo "  1. Open http://localhost:8080 in your browser"
echo "  2. Find 'apod_etl_pipeline' DAG"
echo "  3. Click the play button to trigger"
echo "  4. Watch the execution in Graph View"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f airflow"
echo ""
echo "To stop services:"
echo "  docker-compose down"
echo ""
