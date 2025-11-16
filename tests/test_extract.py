import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'airflow', 'plugins', 'scripts'))

from extract_apod import extract_apod


class TestExtractAPOD(unittest.TestCase):
    """Test cases for APOD data extraction"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_response = {
            'date': '2024-01-15',
            'title': 'Test Image Title',
            'url': 'https://example.com/image.jpg',
            'explanation': 'This is a test explanation',
            'media_type': 'image'
        }

    @patch('extract_apod.requests.get')
    def test_extract_apod_success(self, mock_get):
        """Test successful APOD data extraction"""
        # Mock the API response
        mock_get.return_value = MagicMock()
        mock_get.return_value.json.return_value = self.mock_response
        mock_get.return_value.raise_for_status = MagicMock()

        # Create mock context
        mock_context = {
            'ti': MagicMock()
        }

        # Call the function
        extract_apod(**mock_context)

        # Verify API was called
        mock_get.assert_called_once()
        
        # Verify XCom was updated
        mock_context['ti'].xcom_push.assert_called()

    @patch('extract_apod.requests.get')
    def test_extract_apod_api_error(self, mock_get):
        """Test extraction with API error"""
        # Mock the API to raise an error
        mock_get.return_value.raise_for_status.side_effect = Exception("API Error")

        # Create mock context
        mock_context = {
            'ti': MagicMock()
        }

        # Verify that exception is raised
        with self.assertRaises(Exception):
            extract_apod(**mock_context)

    def test_extract_apod_data_structure(self):
        """Test that extracted data has required fields"""
        required_fields = ['date', 'title', 'url', 'explanation', 'media_type']
        
        for field in required_fields:
            self.assertIn(field, self.mock_response)


if __name__ == '__main__':
    unittest.main()
