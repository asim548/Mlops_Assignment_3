# 🎓 MLOps Assignment 3: NASA APOD Data Pipeline

A robust, reproducible Extract-Transform-Load (ETL) pipeline built with **Apache Airflow**, **DVC**, **PostgreSQL**, and **Docker** for processing NASA's Astronomy Picture of the Day (APOD) data.

## 📋 Project Overview

This assignment integrates essential MLOps tools within a containerized environment to create a production-ready data pipeline. The pipeline demonstrates:

- **Orchestration Mastery**: Apache Airflow for complex workflows
- **Data Integrity**: Concurrent loading to PostgreSQL and CSV
- **Data Lineage**: DVC for artifact versioning
- **Code Versioning**: Git integration for reproducibility
- **Containerization**: Docker/Docker Compose deployment

## 🏗️ Pipeline Architecture

### Five Sequential Steps:

```
Extract → Transform → Load → DVC Track → Git Commit
```

### Step 1: Data Extraction (E)
- **Source**: NASA APOD API (https://api.nasa.gov/planetary/apod)
- **Output**: Raw JSON file with APOD data
- **Task**: `extract_apod_data`

### Step 2: Data Transformation (T)
- **Input**: Raw JSON from extraction
- **Process**: Extract fields (date, title, url, explanation, media_type)
- **Output**: Cleaned CSV and JSON files
- **Task**: `transform_apod_data`

### Step 3: Data Loading (L)
- **Dual Storage**:
  - PostgreSQL database table
  - Local CSV file (`apod_data.csv`)
- **Conflict Handling**: ON CONFLICT DO UPDATE for duplicate dates
- **Task**: `load_to_postgres`

### Step 4: Data Versioning (DVC)
- **Action**: Track CSV file with DVC
- **Output**: `apod_data.csv.dvc` metadata file
- **Purpose**: Version data artifacts independently
- **Task**: `dvc_track_data`

### Step 5: Code Versioning (Git)
- **Action**: Commit DVC metadata to Git
- **Scope**: Push changes to GitHub repository
- **Purpose**: Link pipeline code to exact data versions
- **Task**: `git_commit_metadata`

## 📁 Project Structure

```
├── airflow/
│   ├── dags/
│   │   └── apod_etl_dag.py              # Main Airflow DAG definition
│   └── plugins/
│       └── scripts/
│           ├── extract_apod.py          # Step 1: Data extraction
│           ├── transform_apod.py        # Step 2: Data transformation
│           ├── load_to_postgres.py      # Step 3: Data loading
│           ├── dvc_track_data.py        # Step 4: DVC versioning
│           └── git_commit_metadata.py   # Step 5: Git integration
├── postgres/
│   └── init.sql                          # PostgreSQL initialization script
├── data/
│   ├── raw/                              # Raw APOD JSON files
│   └── processed/                        # Transformed CSV files
├── tests/
│   ├── test_extract.py                   # Extraction tests
│   ├── test_transform.py                 # Transformation tests
│   └── test_load.py                      # Loading tests
├── dvc.yaml                              # DVC pipeline definition
├── docker-compose.yml                    # Docker Compose configuration
├── Dockerfile                            # Custom Airflow image
├── requirements.txt                      # Python dependencies
└── README.md                             # This file
```

## 🚀 Getting Started

### Prerequisites

- Docker & Docker Compose installed
- NASA API Key (optional, defaults to DEMO_KEY)
- Git repository initialized
- Python 3.10+

### Quick Start

#### 1. Clone the Repository

```bash
git clone https://github.com/asim548/Mlops_Assignment_3.git
cd Mlops_Assignment_3
```

#### 2. Set Environment Variables

```bash
# Create .env file
echo "NASA_API_KEY=your_api_key_here" > .env

# Or use DEMO_KEY (limited requests)
echo "NASA_API_KEY=DEMO_KEY" > .env
```

#### 3. Initialize Git (if not already done)

```bash
git init
git add .
git commit -m "Initial commit: Complete MLOps APOD pipeline"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main
```

#### 4. Build and Start Services

```bash
# Build the custom Airflow image
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f airflow
```

#### 5. Access Airflow UI

- **URL**: http://localhost:8080
- **Username**: admin
- **Password**: admin

#### 6. Trigger the DAG

In Airflow UI:
1. Navigate to DAGs
2. Find `apod_etl_pipeline`
3. Click the play button to trigger manually
4. Monitor execution in the Graph View

### Running Locally (Without Docker)

#### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Initialize Airflow

```bash
# Set Airflow home
export AIRFLOW_HOME=$(pwd)

# Initialize database
airflow db init

# Create admin user
airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com
```

#### 4. Start Airflow Services

```bash
# Terminal 1: Start webserver
airflow webserver -p 8080

# Terminal 2: Start scheduler
airflow scheduler
```

#### 5. Start PostgreSQL

```bash
# Using Docker just for Postgres
docker run --name apod-postgres \
  -e POSTGRES_USER=airflow \
  -e POSTGRES_PASSWORD=airflow \
  -e POSTGRES_DB=airflow \
  -p 5432:5432 \
  -v ./postgres/init.sql:/docker-entrypoint-initdb.d/init.sql \
  -d postgres:15
```

## 📊 Data Flow Diagram

```
NASA APOD API
     ↓
┌─────────────────────┐
│  Extract Task       │ → raw_apod_YYYYMMDD_HHMMSS.json
│  (extract_apod)     │
└─────────────────────┘
     ↓
┌─────────────────────┐
│ Transform Task      │ → apod_transformed.json + apod_data.csv
│ (transform_apod)    │
└─────────────────────┘
     ↓
┌─────────────────────────────────────┐
│      Load Task (Parallel)           │
│   ┌──────────────┐  ┌────────────┐  │
│   │  PostgreSQL  │  │  CSV File  │  │
│   │   Database   │  │   Storage  │  │
│   └──────────────┘  └────────────┘  │
└─────────────────────────────────────┘
     ↓
┌─────────────────────┐
│  DVC Track Task     │ → apod_data.csv.dvc
│  (dvc_track_data)   │
└─────────────────────┘
     ↓
┌─────────────────────┐
│ Git Commit Task     │ → Commit to main branch
│(git_commit_metadata)│
└─────────────────────┘
```

## 🧪 Testing

### Run Unit Tests

```bash
# Activate virtual environment
source venv/Scripts/activate  # On Windows

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_extract.py -v

# Run with coverage
python -m pytest tests/ --cov=airflow/plugins/scripts --cov-report=html
```

### Test Coverage

- **test_extract.py**: API extraction, error handling
- **test_transform.py**: Data transformation, field extraction
- **test_load.py**: Database operations, CSV creation

## 🔧 Configuration Files

### docker-compose.yml
- Defines Airflow and PostgreSQL services
- Network configuration
- Volume mounts
- Environment variables

### Dockerfile
- Based on `apache/airflow:2.9.1-python3.10`
- Installs git, ssh, build tools
- Initializes DVC
- Copies Airflow configuration

### dvc.yaml
- Defines DVC pipeline stages
- Data dependencies and outputs
- Reproducible pipeline execution

### postgres/init.sql
- Creates `apod` table with schema
- Indexes for performance
- Table documentation

## 📦 Dependencies

Key packages in `requirements.txt`:

```
apache-airflow==2.9.1
apache-airflow-providers-postgres
pandas>=1.3.0
requests>=2.26.0
dvc>=2.0.0
dvc[ssh]
psycopg2-binary>=2.9.0
sqlalchemy>=1.4.0
python-dotenv>=0.19.0
```

## 🔐 Environment Variables

```bash
# NASA API Configuration
NASA_API_KEY=your_api_key  # Get from https://api.nasa.gov/

# PostgreSQL Configuration
POSTGRES_DB=airflow
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Airflow Configuration
AIRFLOW__CORE__EXECUTOR=SequentialExecutor
AIRFLOW__CORE__LOAD_EXAMPLES=False
```

## 📈 Monitoring & Logs

### Airflow Logs

```bash
# View DAG logs
docker-compose logs -f airflow

# Inspect task logs
docker exec airflow-apod cat /opt/airflow/logs/apod_etl_pipeline/extract_apod_data/attempt-1.log
```

### PostgreSQL Logs

```bash
docker-compose logs -f postgres
```

### Check Data

```bash
# Access PostgreSQL
docker exec -it postgres psql -U airflow -d airflow

# Query APOD table
SELECT * FROM apod;
SELECT COUNT(*) FROM apod;
```

## 🔄 DVC and Git Workflow

### DVC Commands

```bash
# Initialize DVC (done automatically in pipeline)
dvc init --no-scm

# Add data file to DVC
dvc add data/processed/apod_data.csv

# Track DVC changes
git add data/processed/apod_data.csv.dvc
git commit -m "Update APOD data version"

# Pull data from remote
dvc pull
```

### Git Commands

```bash
# Check git status
git status

# View DVC metadata changes
git diff data/processed/apod_data.csv.dvc

# Push to GitHub
git push origin main
```

## 🐛 Troubleshooting

### Issue: "Failed to connect to PostgreSQL"

**Solution**:
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart PostgreSQL
docker-compose restart postgres

# Check connection
docker exec postgres pg_isready -U airflow
```

### Issue: "DVC command not found"

**Solution**:
```bash
# Reinstall DVC
pip install --upgrade dvc

# Verify installation
dvc version
```

### Issue: "Git authentication failed"

**Solution**:
```bash
# Configure git credentials
git config --global user.email "you@example.com"
git config --global user.name "Your Name"

# Or use SSH keys
ssh-keygen -t ed25519 -C "your_email@example.com"
git remote set-url origin git@github.com:yourusername/repo.git
```

### Issue: "DAG not showing in Airflow"

**Solution**:
```bash
# Check DAG file syntax
python airflow/dags/apod_etl_dag.py

# Restart scheduler
docker-compose restart airflow

# Check logs
docker-compose logs airflow | grep -i dag
```

## 📚 Key Learning Outcomes

✅ **Orchestration Mastery**: Designed complex, dependent workflows using Airflow DAGs  
✅ **Data Integrity**: Implemented concurrent loading to multiple storage systems  
✅ **Data Lineage**: Mastered DVC for artifact versioning and reproducibility  
✅ **Containerization**: Created production-ready Docker setup for deployment  
✅ **MLOps Best Practices**: Implemented testing, monitoring, and version control  

## 🎯 Assignment Checklist

- [x] Step 1: Extract APOD data from NASA API
- [x] Step 2: Transform raw JSON to structured format
- [x] Step 3: Load to PostgreSQL and CSV simultaneously
- [x] Step 4: Version data with DVC
- [x] Step 5: Commit metadata to Git
- [x] DAG executes all 5 steps sequentially
- [x] Docker Compose setup with Airflow + PostgreSQL
- [x] Unit tests for extraction, transformation, loading
- [x] Comprehensive documentation
- [x] Error handling and logging

## 👥 Author

- **Student**: Aaim Shehzad
- **Assignment**: MLOps Assignment 3
- **Deadline**: November 16, 2025

## 🔗 Useful Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [DVC Documentation](https://dvc.org/doc)
- [NASA APOD API](https://api.nasa.gov/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Documentation](https://docs.docker.com/)
