#!/bin/bash
cd /opt/airflow

echo "Running DVC add..."
dvc add data/processed/apod_data.csv

echo "Pushing to DVC remote..."
dvc push

echo "DVC tracking completed."
