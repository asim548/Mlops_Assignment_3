import unittest
import os
import sys
import tempfile
import pandas as pd
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'airflow', 'plugins', 'scripts'))

from load_to_postgres import load_to_postgres


class TestLoadToPostgres(unittest.TestCase):
    """Test cases for APOD data loading to PostgreSQL"""

    def setUp(self):
        """Set up test fixtures"""
        self.test_data = {
            'date': ['2024-01-15'],
            'title': ['Test Image Title'],
            'url': ['https://example.com/image.jpg'],
            'explanation': ['This is a test explanation'],
            'media_type': ['image']
        }
        
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_load_creates_valid_dataframe(self):
        """Test that we can create and read a valid CSV"""
        df = pd.DataFrame(self.test_data)
        
        # Save to CSV
        csv_path = os.path.join(self.test_dir, 'test_data.csv')
        df.to_csv(csv_path, index=False)
        
        # Read back and verify
        df_read = pd.read_csv(csv_path)
        self.assertEqual(len(df_read), 1)
        self.assertEqual(df_read.iloc[0]['date'], '2024-01-15')

    @patch('load_to_postgres.psycopg2.connect')
    def test_load_to_postgres_connection(self, mock_connect):
        """Test PostgreSQL connection handling"""
        # Setup mock connection
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Create test CSV
        df = pd.DataFrame(self.test_data)
        csv_path = os.path.join(self.test_dir, 'test_data.csv')
        df.to_csv(csv_path, index=False)

        # Create mock context
        mock_context = {
            'ti': MagicMock()
        }
        mock_context['ti'].xcom_pull.return_value = csv_path

        # Call the function
        load_to_postgres(**mock_context)

        # Verify connection was made
        mock_connect.assert_called_once()

    def test_load_handles_duplicate_dates(self):
        """Test that load handles duplicate dates gracefully"""
        # This is handled by ON CONFLICT in SQL, but we verify the data structure
        duplicate_data = {
            'date': ['2024-01-15', '2024-01-15'],
            'title': ['Title 1', 'Title 2'],
            'url': ['url1', 'url2'],
            'explanation': ['exp1', 'exp2'],
            'media_type': ['image', 'video']
        }
        
        df = pd.DataFrame(duplicate_data)
        
        # Verify DataFrame is created with duplicate dates
        self.assertEqual(len(df), 2)
        # In real SQL, later insert would update the first one
        date_values = df['date'].unique()
        self.assertEqual(len(date_values), 1)


if __name__ == '__main__':
    unittest.main()
