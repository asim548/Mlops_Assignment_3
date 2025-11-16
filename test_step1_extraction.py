#!/usr/bin/env python3
"""
Test Step 1: Data Extraction
Extracts NASA APOD data from public API endpoint
"""

import requests
import json
import os
from datetime import datetime

def step1_extraction():
    """Execute Step 1: Data Extraction"""
    print('='*70)
    print('STEP 1: DATA EXTRACTION (E)')
    print('='*70)
    print()
    
    # API Configuration
    api_key = 'DEMO_KEY'
    url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
    
    print('🔗 Connecting to NASA APOD endpoint...')
    print(f'   URL: {url}')
    print()
    
    try:
        # Make API request
        print('📡 Sending HTTP GET request...')
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse response
        data = response.json()
        print(f'✓ HTTP Status: {response.status_code} OK')
        print()
        
        # Create data directory
        os.makedirs('data/raw', exist_ok=True)
        
        # Save raw JSON with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        raw_path = f'data/raw/apod_raw_{timestamp}.json'
        
        with open(raw_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        print(f'✓ Raw data saved to: {raw_path}')
        print()
        
        # Display extracted data
        print('📊 EXTRACTED DATA:')
        print(f'   Date: {data.get("date")}')
        print(f'   Title: {data.get("title")}')
        print(f'   URL: {data.get("url")}')
        print(f'   Media Type: {data.get("media_type")}')
        print(f'   Explanation (first 100 chars): {data.get("explanation", "")[:100]}...')
        print()
        
        # Verify required fields
        required_fields = ['date', 'title', 'url', 'explanation', 'media_type']
        missing_fields = [f for f in required_fields if f not in data]
        
        if missing_fields:
            print(f'⚠️  WARNING: Missing fields: {missing_fields}')
        else:
            print('✓ All required fields present')
        
        print()
        print('='*70)
        print('✅ STEP 1 EXTRACTION COMPLETED SUCCESSFULLY')
        print('='*70)
        print()
        
        return {
            'status': 'success',
            'raw_path': raw_path,
            'data': data
        }
        
    except requests.exceptions.RequestException as e:
        print(f'❌ ERROR: API request failed - {str(e)}')
        print()
        print('='*70)
        print('❌ STEP 1 EXTRACTION FAILED')
        print('='*70)
        return {'status': 'error', 'error': str(e)}

if __name__ == '__main__':
    result = step1_extraction()
    exit(0 if result['status'] == 'success' else 1)
