import requests
import json
import os
from datetime import datetime

def extract_apod(**context):
    """
    Extract APOD data from NASA API.
    Retrieves: date, title, url, explanation, media_type
    """
    api_key = os.getenv("NASA_API_KEY", "DEMO_KEY")
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}"

    response = requests.get(url)
    response.raise_for_status()   # ensures pipeline fails on API error

    data = response.json()

    # Save raw JSON data for next step
    os.makedirs("/opt/airflow/data/raw", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_path = f"/opt/airflow/data/raw/apod_raw_{timestamp}.json"

    with open(raw_path, "w") as f:
        json.dump(data, f, indent=4)

    # Push path to XCom
    ti = context['ti']
    ti.xcom_push(key='raw_apod_path', value=raw_path)

    print(f"APOD data extracted successfully to {raw_path}")
    print(f"Data: {data.get('date')} - {data.get('title')}")
