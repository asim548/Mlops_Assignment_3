-- Initialize PostgreSQL database for APOD ETL Pipeline

-- Create APOD table
CREATE TABLE IF NOT EXISTS apod (
    date TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT,
    explanation TEXT,
    media_type TEXT DEFAULT 'image',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_apod_date ON apod(date);

-- Add comment
COMMENT ON TABLE apod IS 'NASA APOD (Astronomy Picture of the Day) data extracted and processed by Airflow pipeline';
