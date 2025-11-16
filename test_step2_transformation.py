#!/usr/bin/env python3
"""
Test Step 2: Data Transformation
Transforms raw JSON to structured CSV/JSON format
"""

import json
import pandas as pd
import os
from datetime import datetime
from pathlib import Path

def step2_transformation(raw_path):
    """Execute Step 2: Data Transformation"""
    print('='*70)
    print('STEP 2: DATA TRANSFORMATION (T)')
    print('='*70)
    print()
    
    print(f'📥 Reading raw data from: {raw_path}')
    
    try:
        # Read raw JSON
        with open(raw_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        print('✓ Raw data loaded successfully')
        print()
        
        # Extract required fields
        print('🔄 Extracting fields...')
        extracted_data = {
            'date': raw_data.get('date'),
            'title': raw_data.get('title'),
            'url': raw_data.get('url'),
            'explanation': raw_data.get('explanation'),
            'media_type': raw_data.get('media_type', 'image')
        }
        
        print(f'✓ Extracted 5 fields:')
        for key, value in extracted_data.items():
            if key == 'explanation':
                print(f'  - {key}: {str(value)[:50]}...')
            else:
                print(f'  - {key}: {value}')
        print()
        
        # Create DataFrame
        print('📊 Creating structured DataFrame...')
        df = pd.DataFrame([extracted_data])
        
        print('✓ DataFrame created with shape:', df.shape)
        print()
        
        # Create processed data directory
        os.makedirs('data/processed', exist_ok=True)
        
        # Save as CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_path = 'data/processed/apod_data.csv'
        df.to_csv(csv_path, index=False)
        
        print(f'📁 CSV saved to: {csv_path}')
        print()
        
        # Save as JSON
        json_path = f'data/processed/apod_transformed_{timestamp}.json'
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump([extracted_data], f, indent=4)
        
        print(f'📁 JSON saved to: {json_path}')
        print()
        
        # Display transformed data
        print('📋 TRANSFORMED DATA (CSV format):')
        print(df.to_string(index=False))
        print()
        
        # Verify data structure
        print('✓ Data validation:')
        print(f'  - Records: {len(df)}')
        print(f'  - Columns: {list(df.columns)}')
        print(f'  - Data types:')
        for col, dtype in df.dtypes.items():
            print(f'    • {col}: {dtype}')
        print()
        
        print('='*70)
        print('✅ STEP 2 TRANSFORMATION COMPLETED SUCCESSFULLY')
        print('='*70)
        print()
        
        return {
            'status': 'success',
            'csv_path': csv_path,
            'json_path': json_path,
            'dataframe': df,
            'data': extracted_data
        }
        
    except Exception as e:
        print(f'❌ ERROR during transformation: {str(e)}')
        print()
        print('='*70)
        print('❌ STEP 2 TRANSFORMATION FAILED')
        print('='*70)
        return {'status': 'error', 'error': str(e)}

if __name__ == '__main__':
    # Find the latest raw data file
    raw_dir = Path('data/raw')
    if raw_dir.exists():
        raw_files = sorted(list(raw_dir.glob('*.json')), reverse=True)
        if raw_files:
            result = step2_transformation(str(raw_files[0]))
            exit(0 if result['status'] == 'success' else 1)
        else:
            print('❌ No raw data files found in data/raw/')
            exit(1)
    else:
        print('❌ data/raw directory not found')
        exit(1)
