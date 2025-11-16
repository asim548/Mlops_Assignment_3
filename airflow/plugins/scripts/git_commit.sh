#!/bin/bash
cd /opt/airflow

git config --global user.email "airflow@pipeline.com"
git config --global user.name "Airflow Pipeline"

git add data/processed/apod_data.csv.dvc
git commit -m "Updated APOD dataset version"
git push origin main

echo "Git commit + push completed."
