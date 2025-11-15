# MLOps APOD ETL Pipeline

This project implements a complete MLOps data ingestion pipeline using:

- Apache Airflow (ETL Orchestration)
- DVC (Data Version Control)
- GitHub (Code + Data Metadata Versioning)
- Postgres (Data Warehouse)
- Docker / Astronomer (Containerized Deployment)

## Pipeline Steps

### 1. Extract
Fetch NASA APOD (Astronomy Picture of the Day) data using:
https://api.nasa.gov/planetary/apod

### 2. Transform
Select fields:
- date
- title
- url
- explanation

Convert JSON → Pandas DataFrame → CSV.

### 3. Load
Load cleaned data into:
- Postgres table (apod)
- data/processed/apod_data.csv

### 4. DVC Tracking
Run:
