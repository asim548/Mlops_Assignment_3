"""
APOD ETL Pipeline DAG
Orchestrates a complete Extract-Transform-Load pipeline for NASA APOD data
with DVC versioning and Git integration.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.utils.dates import days_ago

from airflow.plugins.scripts.extract_apod import extract_apod
from airflow.plugins.scripts.transform_apod import transform_apod
from airflow.plugins.scripts.load_to_postgres import load_to_postgres
from airflow.plugins.scripts.dvc_track_data import dvc_track_data
from airflow.plugins.scripts.git_commit_metadata import git_commit_dvc_metadata

# DAG Configuration
default_args = {
    'owner': 'mlops_team',
    'retries': 1,
    'start_date': days_ago(1),
}

with DAG(
    dag_id="apod_etl_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
    description="NASA APOD ETL Pipeline with DVC and Git Integration",
) as dag:

    # Step 1: Extract - Fetch data from NASA APOD API
    extract_task = PythonOperator(
        task_id="extract_apod_data",
        python_callable=extract_apod,
        provide_context=True,
        doc="Extract APOD data from NASA API"
    )

    # Step 2: Transform - Process and structure the data
    transform_task = PythonOperator(
        task_id="transform_apod_data",
        python_callable=transform_apod,
        provide_context=True,
        doc="Transform raw JSON to structured format (CSV + JSON)"
    )

    # Step 3: Load - Persist to PostgreSQL and local CSV
    load_task = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_to_postgres,
        provide_context=True,
        doc="Load data into PostgreSQL database"
    )

    # Step 4: DVC Track - Version the data with DVC
    dvc_task = PythonOperator(
        task_id="dvc_track_data",
        python_callable=dvc_track_data,
        provide_context=True,
        doc="Track data artifacts with DVC for versioning"
    )

    # Step 5: Git Commit - Commit DVC metadata to Git
    git_task = PythonOperator(
        task_id="git_commit_metadata",
        python_callable=git_commit_dvc_metadata,
        provide_context=True,
        doc="Commit DVC metadata to Git repository"
    )

    # Define task dependencies: Sequential execution
    extract_task >> transform_task >> load_task >> dvc_task >> git_task

