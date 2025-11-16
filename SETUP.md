# 🚀 Complete Setup Guide for MLOps Assignment 3

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Docker Setup (Recommended)](#docker-setup-recommended)
3. [Local Setup](#local-setup)
4. [Verification Steps](#verification-steps)
5. [Triggering the Pipeline](#triggering-the-pipeline)
6. [Monitoring & Debugging](#monitoring--debugging)

## Prerequisites

### System Requirements
- **OS**: Windows 10/11, macOS, or Linux
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Disk Space**: 10GB free space
- **Internet**: Active internet connection

### Required Software
- [Docker Desktop](https://www.docker.com/products/docker-desktop) (20.10+)
- [Git](https://git-scm.com/) (2.25+)
- [Python](https://www.python.org/downloads/) (3.10+) - for local setup only

### NASA API Key (Optional)
- Get free API key at: https://api.nasa.gov/
- If not provided, pipeline uses DEMO_KEY (limited requests)

---

## Docker Setup (Recommended)

### Step 1: Clone and Navigate

```bash
# Clone repository
git clone https://github.com/asim548/Mlops_Assignment_3.git
cd Mlops_Assignment_3

# Or if already in the folder
cd c:\Users\Aaim Shehzad\OneDrive\Desktop\7\MLOPs\Mlops_22i_2679_A3
```

### Step 2: Configure Environment

```bash
# Windows PowerShell
$env:NASA_API_KEY = "DEMO_KEY"

# Or create .env file
"NASA_API_KEY=DEMO_KEY" | Out-File .env
```

### Step 3: Build Docker Image

```bash
# Build custom Airflow image with all dependencies
docker-compose build --no-cache
```

### Step 4: Start Services

```bash
# Start all services (Postgres + Airflow)
docker-compose up -d

# View startup logs
docker-compose logs -f

# Wait for Airflow to be ready (1-2 minutes)
```

### Step 5: Initialize Airflow

```bash
# Create admin user (if not already created)
docker-compose exec airflow airflow users create `
  --username admin `
  --password admin `
  --firstname Admin `
  --lastname User `
  --role Admin `
  --email admin@example.com
```

### Step 6: Access Airflow UI

- **URL**: http://localhost:8080
- **Username**: admin
- **Password**: admin

---

## Local Setup

### Step 1: Create Virtual Environment

```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Initialize Airflow

```bash
# Set Airflow home
$env:AIRFLOW_HOME = (Get-Location).Path

# Initialize database
airflow db init

# Create admin user
airflow users create `
  --username admin `
  --password admin `
  --firstname Admin `
  --lastname User `
  --role Admin `
  --email admin@example.com
```

### Step 4: Set Environment Variables

```bash
# Windows PowerShell
$env:NASA_API_KEY = "DEMO_KEY"
$env:POSTGRES_HOST = "localhost"
$env:POSTGRES_USER = "airflow"
$env:POSTGRES_PASSWORD = "airflow"
$env:POSTGRES_DB = "airflow"
$env:POSTGRES_PORT = "5432"
```

### Step 5: Start PostgreSQL

```bash
# Using Docker for just PostgreSQL
docker run --name apod-postgres `
  -e POSTGRES_USER=airflow `
  -e POSTGRES_PASSWORD=airflow `
  -e POSTGRES_DB=airflow `
  -p 5432:5432 `
  -v ${PWD}/postgres/init.sql:/docker-entrypoint-initdb.d/init.sql `
  -d postgres:15

# Verify connection
docker exec apod-postgres pg_isready -U airflow
```

### Step 6: Start Airflow

```bash
# Terminal 1: Start Webserver
airflow webserver -p 8080

# Terminal 2: Start Scheduler
airflow scheduler

# Airflow UI will be available at http://localhost:8080
```

---

## Verification Steps

### Check Docker Services

```bash
# Verify containers are running
docker-compose ps

# Should show:
# airflow (running)
# postgres (running)
```

### Check Airflow UI

1. Open http://localhost:8080
2. Login with admin/admin
3. Go to **Admin** → **Connections** → Verify postgres connection

### Verify PostgreSQL

```bash
# Connect to database
docker exec -it postgres psql -U airflow -d airflow

# Inside psql prompt
\dt              # List tables
SELECT * FROM apod LIMIT 1;  # Query APOD table
\q               # Exit
```

### Check File Structure

```bash
# Verify data directories are created
ls -la data/
ls -la data/raw/
ls -la data/processed/

# Should see these directories created during first run
```

---

## Triggering the Pipeline

### Method 1: Using Airflow UI (Recommended)

1. Go to http://localhost:8080
2. Find **apod_etl_pipeline** in the DAG list
3. Click the **Play** button (▶️) to trigger
4. Select **Trigger DAG** with default configuration
5. Watch the execution in **Graph View**

### Method 2: Using Command Line

```bash
# Trigger DAG manually
airflow dags trigger apod_etl_pipeline

# Or with custom execution date
airflow dags trigger apod_etl_pipeline --exec-date 2024-01-15
```

### Method 3: Automatic Daily Schedule

The DAG is configured to run automatically at midnight daily via the `@daily` schedule.

---

## Monitoring & Debugging

### View DAG Execution

```bash
# List all DAG runs
airflow dags list-runs --dag-id apod_etl_pipeline

# Get DAG details
airflow dags info apod_etl_pipeline
```

### Check Task Logs

```bash
# View logs for a specific task
airflow tasks logs apod_etl_pipeline extract_apod_data 2024-01-15T00:00:00Z

# Or in Docker
docker exec airflow airflow tasks logs apod_etl_pipeline extract_apod_data 2024-01-15T00:00:00Z
```

### Debug DAG Syntax

```bash
# Validate DAG file
python airflow/dags/apod_etl_dag.py

# If no error output, DAG is valid
```

### Check Data Files

```bash
# List raw data
ls -la data/raw/

# List processed data
ls -la data/processed/

# View CSV content
cat data/processed/apod_data.csv
```

### View Database Data

```bash
# Access PostgreSQL
docker exec -it postgres psql -U airflow -d airflow

# Check APOD table
SELECT COUNT(*) FROM apod;
SELECT * FROM apod ORDER BY created_at DESC LIMIT 1;

# Check table schema
\d apod
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart airflow
docker-compose restart postgres

# Rebuild from scratch
docker-compose down
docker-compose up -d --build
```

---

## Common Issues & Solutions

### Issue: "Waiting for scheduler to catch up"

**Solution**: Wait 2-3 minutes, or:
```bash
# Restart scheduler
docker-compose restart airflow
docker-compose logs -f airflow
```

### Issue: "Database locked"

**Solution**:
```bash
# Stop all services
docker-compose down

# Start fresh
docker-compose up -d
```

### Issue: "Connection refused"

**Solution**:
```bash
# Check if PostgreSQL is ready
docker-compose logs postgres

# Wait for health check to pass
docker exec postgres pg_isready -U airflow
```

### Issue: "DVC command not found"

**Solution**:
```bash
# For Docker setup
docker-compose exec airflow pip install --upgrade dvc

# For local setup
pip install --upgrade dvc
```

---

## Next Steps After Setup

1. **Verify Pipeline**: Trigger DAG and monitor execution
2. **Check Data**: Query PostgreSQL for loaded data
3. **Review Logs**: Check task logs for any errors
4. **Test Components**: Run unit tests
5. **Push to GitHub**: Commit changes and push to repository

```bash
# Test locally
pytest tests/ -v

# Commit changes
git add .
git commit -m "Initial MLOps APOD pipeline setup"
git push origin main
```

---

## Support Commands

```bash
# Check Airflow version
airflow version

# List installed packages
pip list | grep -E "(airflow|dvc|postgres|pandas)"

# Check Docker version
docker --version
docker-compose --version

# View all containers
docker ps -a

# View container resource usage
docker stats
```

---

## Cleanup (If Needed)

```bash
# Stop all containers
docker-compose stop

# Remove containers
docker-compose down

# Remove volumes (WARNING: Deletes all data)
docker-compose down -v

# Remove images
docker-compose down -v --remove-orphans
```

---

## Next: Assignment Submission

When ready to submit:

1. Ensure all 5 pipeline steps work successfully
2. Push code to GitHub
3. Verify DAG runs without errors
4. Document any issues faced and solutions
5. Prepare screenshots of:
   - Airflow DAG Graph
   - Successful task execution
   - PostgreSQL data
   - GitHub commits with .dvc files

---

**Good luck! 🚀**
