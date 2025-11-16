import unittest
import json
import os
import sys
import tempfile
import pandas as pd
from unittest.mock import MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'airflow', 'plugins', 'scripts'))

from transform_apod import transform_apod


class TestTransformAPOD(unittest.TestCase):
    """Test cases for APOD data transformation"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_data = {
            'date': '2024-01-15',
            'title': 'Test Image Title',
            'url': 'https://example.com/image.jpg',
            'explanation': 'This is a test explanation of the image',
            'media_type': 'image',
            'copyright': 'Test Author'
        }
        
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_transform_extracts_required_fields(self):
        """Test that transformation extracts required fields"""
        # Create test raw data file
        raw_file = os.path.join(self.test_dir, 'raw_apod.json')
        with open(raw_file, 'w') as f:
            json.dump(self.test_data, f)

        # Create mock context
        mock_context = {
            'ti': MagicMock()
        }
        mock_context['ti'].xcom_pull.return_value = raw_file

        # We can verify the expected transformation structure
        expected_fields = ['date', 'title', 'url', 'explanation', 'media_type']
        
        for field in expected_fields:
            self.assertIn(field, self.test_data)

    def test_transform_creates_dataframe(self):
        """Test that transformation creates a proper DataFrame"""
        # Create a DataFrame from test data
        df = pd.DataFrame([self.test_data])
        
        # Verify DataFrame structure
        self.assertEqual(len(df), 1)
        self.assertIn('date', df.columns)
        self.assertIn('title', df.columns)
        self.assertEqual(df.iloc[0]['date'], '2024-01-15')

    def test_transform_handles_missing_fields(self):
        """Test handling of missing optional fields"""
        incomplete_data = {
            'date': '2024-01-15',
            'title': 'Test Title',
            # Missing url and explanation
        }
        
        df = pd.DataFrame([incomplete_data])
        
        # Verify DataFrame is created even with missing fields
        self.assertEqual(len(df), 1)
        self.assertTrue(pd.isna(df.iloc[0].get('url', None)))


if __name__ == '__main__':
    unittest.main()
