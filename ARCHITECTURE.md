# 📐 MLOps APOD Pipeline - Architecture & Design Document

## Executive Summary

The APOD (Astronomy Picture of the Day) ETL Pipeline is a production-ready data ingestion system demonstrating enterprise MLOps best practices. It seamlessly integrates:

- **Workflow Orchestration**: Apache Airflow
- **Data Versioning**: DVC (Data Version Control)
- **Data Persistence**: PostgreSQL
- **Containerization**: Docker & Docker Compose
- **Version Control**: Git/GitHub

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    External Data Sources                            │
│                                                                      │
│              NASA APOD API (REST Endpoint)                          │
│         https://api.nasa.gov/planetary/apod                         │
└────────────────────────┬────────────────────────────────────────────┘
                         │ (JSON Data)
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│              Apache Airflow Orchestration Layer                      │
│                     (Airflow Scheduler)                             │
│                                                                      │
│  ┌─────────────┬─────────────┬─────────────┬───────────┬────────┐  │
│  │  Extract    │  Transform  │   Load      │  DVC      │  Git   │  │
│  │   Task      │    Task     │   Task      │  Track    │  Commit│  │
│  │             │             │             │  Task     │ Task   │  │
│  └─────┬───────┴─────┬───────┴──────┬──────┴─────┬─────┴────┬───┘  │
│        │             │              │            │          │      │
└────────┼─────────────┼──────────────┼────────────┼──────────┼──────┘
         │             │              │            │          │
         ▼             ▼              ▼            ▼          ▼
    ┌─────────────────────────────────────────────────────────────┐
    │          Data Storage & Version Control Layer               │
    │                                                             │
    │  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐   │
    │  │  PostgreSQL  │  │ DVC Metadata │  │   Git Repo    │   │
    │  │   Database   │  │   Storage    │  │   (.dvc files)│   │
    │  │              │  │              │  │               │   │
    │  │  ┌────────┐  │  │ data/        │  │  Commits:     │   │
    │  │  │apod    │  │  │ processed/   │  │  - apod_data. │   │
    │  │  │ table  │  │  │ apod_data.   │  │    csv.dvc    │   │
    │  │  └────────┘  │  │ csv.dvc      │  │  - code       │   │
    │  │              │  │              │  │    changes    │   │
    │  └──────────────┘  └──────────────┘  └───────────────┘   │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
         │
         ▼
    ┌─────────────────────────────────────────────────────────────┐
    │          Local File Storage Layer                           │
    │                                                             │
    │  /opt/airflow/data/                                         │
    │  ├── raw/                                                   │
    │  │   └── apod_raw_YYYYMMDD_HHMMSS.json                     │
    │  └── processed/                                             │
    │      ├── apod_data.csv                                      │
    │      ├── apod_data.csv.dvc                                  │
    │      └── apod_transformed.json                              │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. Extraction Layer (`extract_apod.py`)

**Purpose**: Fetch raw APOD data from NASA API

**Responsibilities**:
- Connect to NASA APOD endpoint
- Retrieve daily picture metadata
- Validate API response
- Save raw JSON to `/opt/airflow/data/raw/`
- Push file path to XCom

**Output**:
```
{
  "date": "2024-01-15",
  "title": "Image Title",
  "url": "https://apod.nasa.gov/apod/image/...",
  "explanation": "Detailed description...",
  "media_type": "image",
  "copyright": "Photographer Name"
}
```

**Error Handling**:
- API connection failures → Task retry
- Invalid response → Task failure
- HTTP errors → Caught and logged

### 2. Transformation Layer (`transform_apod.py`)

**Purpose**: Clean and structure raw data

**Responsibilities**:
- Read raw JSON from previous step
- Extract specific fields of interest
- Create Pandas DataFrame
- Save as CSV and JSON
- Push paths to XCom

**Transformations**:
```
Input Fields  →  Output Fields
date          →  date
title         →  title
url           →  url
explanation   →  explanation
media_type    →  media_type
copyright     →  (filtered out)
```

**Output Files**:
1. `/opt/airflow/data/processed/apod_data.csv` - CSV format for easy analysis
2. `/opt/airflow/data/processed/apod_transformed.json` - Structured JSON

### 3. Loading Layer (`load_to_postgres.py`)

**Purpose**: Persist data to multiple destinations

**Responsibilities**:
- Read transformed CSV
- Connect to PostgreSQL
- Create `apod` table if needed
- Insert/update data
- Handle duplicates gracefully

**Database Schema**:
```sql
CREATE TABLE apod (
    date TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT,
    explanation TEXT,
    media_type TEXT DEFAULT 'image',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Conflict Resolution**:
```sql
ON CONFLICT (date) DO UPDATE SET
    title = EXCLUDED.title,
    url = EXCLUDED.url,
    explanation = EXCLUDED.explanation,
    media_type = EXCLUDED.media_type;
```

### 4. Versioning Layer - DVC (`dvc_track_data.py`)

**Purpose**: Version data artifacts independently

**Responsibilities**:
- Initialize DVC (if not already done)
- Track CSV file with `dvc add`
- Create `.dvc` metadata file
- Push path to XCom

**Generated Files**:
- `data/processed/apod_data.csv.dvc` - Metadata file tracking data hash and remote location

**Benefits**:
- Data versioning without bloating Git
- Reproducible data pipelines
- Data lineage tracking

### 5. Git Integration (`git_commit_metadata.py`)

**Purpose**: Link code changes to data versions

**Responsibilities**:
- Configure Git user (if needed)
- Stage DVC metadata files
- Create commit with DVC changes
- Push to remote repository

**Commit Information**:
```
commit: "Update DVC metadata: data/processed/apod_data.csv.dvc"
Author: Airflow Pipeline <airflow@mlops.local>
Content: DVC metadata reflecting current data version
```

## Orchestration Flow (DAG)

### Linear Pipeline Execution

```
Task: extract_apod_data
├─ Duration: 2-5 seconds
├─ Output: raw JSON file
└─ On Success → transform_apod_data
   │
   └─ Task: transform_apod_data
      ├─ Duration: 1-2 seconds
      ├─ Output: CSV + JSON files
      └─ On Success → load_to_postgres
         │
         └─ Task: load_to_postgres
            ├─ Duration: 2-3 seconds
            ├─ Output: DB records
            └─ On Success → dvc_track_data
               │
               └─ Task: dvc_track_data
                  ├─ Duration: 3-5 seconds
                  ├─ Output: .dvc metadata
                  └─ On Success → git_commit_metadata
                     │
                     └─ Task: git_commit_metadata
                        ├─ Duration: 2-4 seconds
                        ├─ Output: Git commit
                        └─ Complete ✓
```

### Execution Context (XCom)

Tasks communicate via XCom (Cross-Communication):

```
extract_apod_data pushes:
├─ raw_apod_path: "/opt/airflow/data/raw/apod_raw_20240115_120000.json"

transform_apod_data pulls raw_apod_path, pushes:
├─ transformed_csv_path: "/opt/airflow/data/processed/apod_data.csv"
├─ transformed_json_path: "/opt/airflow/data/processed/apod_transformed.json"
├─ transformed_df_json: "[{...}]" (DataFrame as JSON)

load_to_postgres pulls transformed_csv_path

dvc_track_data pulls transformed_csv_path, pushes:
├─ dvc_file_path: "data/processed/apod_data.csv.dvc"

git_commit_metadata pulls dvc_file_path
```

## Data Flow Diagram

### Step-by-Step Data Journey

```
1. EXTRACTION
   NASA API
       ↓
   requests.get()
       ↓
   JSON Response
       ↓
   Write to file
       ↓
   /opt/airflow/data/raw/apod_raw_*.json

2. TRANSFORMATION
   Read raw JSON
       ↓
   Extract fields
       ↓
   Create DataFrame
       ↓
   Write CSV & JSON
       ↓
   /opt/airflow/data/processed/apod_data.csv
   /opt/airflow/data/processed/apod_transformed.json

3. LOADING
   Read CSV
       ↓
   Connect to Postgres
       ├─ CREATE TABLE IF NOT EXISTS
       └─ INSERT/UPDATE data
       ↓
   Database updated
       ↓
   PostgreSQL:apod table

4. DVC VERSIONING
   dvc add CSV
       ↓
   Calculate MD5 hash
       ↓
   Create metadata
       ↓
   /opt/airflow/data/processed/apod_data.csv.dvc

5. GIT INTEGRATION
   git config user
       ↓
   git add *.dvc
       ↓
   git commit
       ↓
   git push origin main
       ↓
   GitHub updated
```

## Storage Architecture

### Local File System

```
/opt/airflow/
├── data/
│   ├── raw/                              (Auto-created)
│   │   └── apod_raw_20240115_*.json      (1-10 MB per run)
│   │
│   └── processed/                        (Auto-created)
│       ├── apod_data.csv                 (1-5 KB)
│       ├── apod_data.csv.dvc             (~1 KB)
│       └── apod_transformed.json         (5-10 KB)
│
├── logs/                                  (Airflow logs)
│   └── apod_etl_pipeline/                (Auto-created)
│       ├── extract_apod_data/
│       ├── transform_apod_data/
│       ├── load_to_postgres/
│       ├── dvc_track_data/
│       └── git_commit_metadata/
│
└── plugins/
    └── scripts/
        ├── extract_apod.py
        ├── transform_apod.py
        ├── load_to_postgres.py
        ├── dvc_track_data.py
        └── git_commit_metadata.py
```

### Database Schema

```sql
Database: airflow
├── Table: apod
│   ├── PK: date (TEXT)
│   ├── title (TEXT, NOT NULL)
│   ├── url (TEXT)
│   ├── explanation (TEXT)
│   ├── media_type (TEXT, DEFAULT 'image')
│   ├── created_at (TIMESTAMP, DEFAULT NOW())
│   └── updated_at (TIMESTAMP, DEFAULT NOW())
│
├── Index: idx_apod_date
│   └── On: date (for fast lookups)
│
└── Constraints:
    └── UNIQUE(date) → ON CONFLICT DO UPDATE
```

### DVC Metadata Structure

```
data/processed/apod_data.csv.dvc (YAML format):

outs:
- path: data/processed/apod_data.csv
  hash: md5
  md5: 1a2b3c4d5e6f7g8h9i0j
  size: 2048
  nfiles: 1

deps: []
```

## Containerization Architecture

### Docker Image Layers

```
Layer 1: apache/airflow:2.9.1-python3.10
├── Python 3.10
├── Airflow 2.9.1
└── Basic dependencies

Layer 2: System packages
├── git
├── ssh
├── build-essential
└── libpq-dev

Layer 3: Python packages
├── apache-airflow-providers-postgres
├── pandas
├── requests
├── dvc[ssh]
├── psycopg2-binary
├── sqlalchemy
└── python-dotenv

Layer 4: Application code
├── airflow/dags/
├── airflow/plugins/scripts/
└── Configuration files

Final: Service ports
└── 8080 (Airflow WebUI)
```

### Docker Compose Services

```yaml
services:
  ├── postgres
  │   ├── Image: postgres:15
  │   ├── Ports: 5432:5432
  │   ├── Volume: postgres_data:/var/lib/postgresql/data
  │   └── Env: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
  │
  └── airflow
      ├── Build: ./Dockerfile
      ├── Ports: 8080:8080
      ├── Volumes: ./airflow:/opt/airflow, ./data:/opt/airflow/data
      ├── Depends: postgres (healthcheck)
      └── Env: AIRFLOW__*, NASA_API_KEY, POSTGRES_*
```

## Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Orchestration** | Apache Airflow | 2.9.1 | DAG scheduling and execution |
| **Data Processing** | Python/Pandas | 3.10/1.3+ | Data transformation |
| **API Client** | Requests | 2.26+ | NASA API calls |
| **Database** | PostgreSQL | 15 | Data warehouse |
| **Python Driver** | psycopg2-binary | 2.9+ | DB connectivity |
| **Versioning** | DVC | 2.0+ | Data artifact versioning |
| **SCM** | Git | 2.25+ | Code versioning |
| **Containerization** | Docker | 20.10+ | Image building |
| **Orchestration** | Docker Compose | 1.29+ | Multi-container setup |

## Security Considerations

### API Key Management
- **Method**: Environment variables
- **Storage**: `.env` file (NOT committed to Git)
- **Rotation**: Support for key rotation via UI update

### Database Security
- **Authentication**: User/password combination
- **Connection**: Can use SSL/TLS (configurable)
- **Separation**: Airflow and app-specific credentials

### Git Integration
- **Authentication**: SSH keys or credentials
- **Scope**: Metadata files only (no sensitive data)
- **Logging**: Git operations logged for audit trail

## Performance Considerations

### Pipeline Duration
- **Typical Total Time**: 15-25 seconds end-to-end
  - Extract: 2-5 sec (API latency)
  - Transform: 1-2 sec (DataFrame creation)
  - Load: 2-3 sec (DB insertion)
  - DVC Track: 3-5 sec (Hash calculation)
  - Git Commit: 2-4 sec (Remote push)

### Scalability Factors
- **Concurrency**: Sequential execution (can be parallelized)
- **Data Volume**: Handles 1-100 MB daily records easily
- **Database**: PostgreSQL can handle millions of records
- **Storage**: Unlimited with DVC remote storage

## Monitoring & Observability

### Airflow UI Monitoring
- DAG execution status
- Task duration tracking
- Real-time log viewing
- XCom value inspection

### Logging
- **Airflow Logs**: `/opt/airflow/logs/apod_etl_pipeline/`
- **Database Logs**: PostgreSQL application log
- **DVC Logs**: Captured in task logs

### Health Checks
- Postgres connection health check
- Task failure retry mechanism
- Alert-on-failure support

## Disaster Recovery

### Data Backup Strategy
- **Raw Data**: Versioned with DVC
- **Processed Data**: Backed up in PostgreSQL
- **Metadata**: Git history for complete lineage

### Recovery Procedures
```
If data is lost:
1. Retrieve version from DVC remote
2. Re-run transform step
3. Reload to PostgreSQL
4. New commit created automatically

If database fails:
1. Restore from backup
2. Re-run load task
3. DVC ensures data consistency
```

## Future Enhancements

### Potential Improvements
- [ ] Parallel loading (simultaneous DB + S3 writes)
- [ ] Data quality checks (validation step)
- [ ] Alerting (email/Slack notifications)
- [ ] Multi-source support (extend beyond APOD)
- [ ] ML model integration (training pipeline)
- [ ] Real-time streaming (Kafka integration)
- [ ] Auto-scaling (Kubernetes deployment)

---

**Architecture Document Version**: 1.0  
**Last Updated**: 2024-01-15  
**Status**: Production Ready ✓
