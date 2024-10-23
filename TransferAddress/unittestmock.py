import unittest
from unittest.mock import patch, MagicMock, Mock
from app import app
from unittest import TestCase


class Test(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.get_db')  # using @patch to replace get_db function(in app.py)
    def test_get_shorten_url_exists(self, mock_get_db):  # mock_get_db is get_db function's action
        mock_collection = Mock()  # Build a mock collection = mock Table
        mock_collection.find_one.return_value = {
            "original_url": "https://uk.indeed.com/jobs?q=junior+software+developer&l=United+Kingdom&sc=0bf%3Aexrec%28%29%3B&start=50&vjk=8a99654d73c1aa63",
            "short_url": "abc"}
        # using the mock collection to find the mock data and return the data which are original data and short data

        mock_get_db.return_value = mock_collection
        # In the app.py we will use get_db function to get the real collection called urls
        # But in here we will not access the actual collection, we will use mock_collection to return value
        response = self.app.post('/shorten', json={
            "original_url": "https://uk.indeed.com/jobs?q=junior+software+developer&l=United+Kingdom&sc=0bf%3Aexrec%28%29%3B&start=50&vjk=8a99654d73c1aa63"})

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"abc", response.data)

    @patch('app.get_db')
    def test_shorten_url_no_original_url(self, mock_get_db):
        mock_collection = Mock()
        mock_get_db.return_value = mock_collection

        response = self.app.post('/shorten', json={'original_url': {}})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
