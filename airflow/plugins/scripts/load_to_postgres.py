import pandas as pd
import psycopg2
import os


def load_to_postgres(**context):
    """
    Load transformed APOD data into PostgreSQL database.
    Creates apod table if it doesn't exist.
    Handles duplicate entries gracefully with ON CONFLICT.
    """
    # Get CSV path from XCom
    ti = context['ti']
    csv_path = ti.xcom_pull(task_ids='transform_apod_data', key='transformed_csv_path')
    
    if not csv_path or not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found at {csv_path}")
    
    # Read the CSV
    df = pd.read_csv(csv_path)

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB", "airflow"),
        user=os.getenv("POSTGRES_USER", "airflow"),
        password=os.getenv("POSTGRES_PASSWORD", "airflow"),
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )

    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS apod (
            date TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT,
            explanation TEXT,
            media_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Insert data with conflict handling
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO apod (date, title, url, explanation, media_type)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (date) DO UPDATE SET
                title = EXCLUDED.title,
                url = EXCLUDED.url,
                explanation = EXCLUDED.explanation,
                media_type = EXCLUDED.media_type;
        """, (
            row["date"],
            row["title"],
            row["url"],
            row["explanation"],
            row.get("media_type", "image")
        ))

    conn.commit()
    cur.close()
    conn.close()

    print("Load Step Completed: Data inserted into PostgreSQL.")
    print(f"Records loaded: {len(df)}")
