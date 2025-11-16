import json
import pandas as pd
import os


def transform_apod(**context):
    """
    Transform raw APOD JSON data into a structured format.
    Extracts: date, title, url, explanation, media_type
    Saves both JSON and CSV formats for flexibility.
    """
    # Get raw data path from XCom
    ti = context['ti']
    raw_path = ti.xcom_pull(task_ids='extract_apod_data', key='raw_apod_path')
    
    if not raw_path or not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw data file not found at {raw_path}")
    
    # Load raw JSON
    with open(raw_path, 'r') as f:
        raw_data = json.load(f)
    
    # Extract specific fields
    transformed_data = {
        'date': raw_data.get('date'),
        'title': raw_data.get('title'),
        'url': raw_data.get('url'),
        'explanation': raw_data.get('explanation'),
        'media_type': raw_data.get('media_type')
    }
    
    # Create DataFrame
    df = pd.DataFrame([transformed_data])
    
    # Save transformed data in processed folder
    os.makedirs("/opt/airflow/data/processed", exist_ok=True)
    
    # Save as CSV
    csv_path = '/opt/airflow/data/processed/apod_data.csv'
    df.to_csv(csv_path, index=False)
    
    # Save as JSON
    json_path = '/opt/airflow/data/processed/apod_transformed.json'
    with open(json_path, 'w') as f:
        json.dump(transformed_data, f, indent=4)
    
    # Push to XCom for next tasks
    ti.xcom_push(key='transformed_csv_path', value=csv_path)
    ti.xcom_push(key='transformed_json_path', value=json_path)
    ti.xcom_push(key='transformed_df_json', value=df.to_json())
    
    print("Transform Step Completed!")
    print(f"CSV Output: {csv_path}")
    print(f"JSON Output: {json_path}")
    print(f"Transformed data:\n{df.to_string()}")
