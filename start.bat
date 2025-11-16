@echo off
REM MLOps APOD Pipeline - Quick Start Script for Windows
REM This script sets up and starts the complete pipeline

setlocal enabledelayedexpansion

echo.
echo ================================================
echo  MLOps APOD ETL Pipeline - Quick Start
echo ================================================
echo.

REM Check if Docker is installed
echo Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    exit /b 1
)

echo Docker found: 
docker --version
echo.

REM Check if Git is installed
echo Checking Git installation...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/
    exit /b 1
)

echo Git found:
git --version
echo.

REM Set environment variables
echo Setting environment variables...
setx NASA_API_KEY "DEMO_KEY"
set NASA_API_KEY=DEMO_KEY

REM Build Docker image
echo.
echo Building Docker image (this may take 5-10 minutes)...
docker-compose build --no-cache
if errorlevel 1 (
    echo ERROR: Docker build failed
    exit /b 1
)

echo Docker build completed successfully!
echo.

REM Start services
echo Starting services (Postgres + Airflow)...
docker-compose up -d

if errorlevel 1 (
    echo ERROR: Failed to start services
    exit /b 1
)

echo.
echo ================================================
echo  ✓ Services started!
echo ================================================
echo.
echo Waiting for services to be ready (30 seconds)...
timeout /t 30 /nobreak

echo.
echo ================================================
echo  Airflow Setup Complete!
echo ================================================
echo.
echo Access Airflow UI:
echo   URL: http://localhost:8080
echo   Username: admin
echo   Password: admin
echo.
echo PostgreSQL:
echo   Host: localhost
echo   Port: 5432
echo   User: airflow
echo   Password: airflow
echo.
echo Next steps:
echo   1. Open http://localhost:8080 in your browser
echo   2. Find 'apod_etl_pipeline' DAG
echo   3. Click the play button to trigger
echo   4. Watch the execution in Graph View
echo.
echo To view logs:
echo   docker-compose logs -f airflow
echo.
echo To stop services:
echo   docker-compose down
echo.
pause
