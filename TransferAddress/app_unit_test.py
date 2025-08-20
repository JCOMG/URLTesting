# tests/test_app.py
import unittest
from unittest.mock import patch, Mock
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from URLTesting.app import app as flask_app


class TestShortener(unittest.TestCase):
    def setUp(self):
        self.client = flask_app.test_client()
        flask_app.testing = True

    @patch('URLTesting.app.get_db', create=True)
    def test_shorten_url_too_long(self, mock_get_db):
        mock_get_db.return_value = Mock()
        very_long = "https://example.com/" + "a" * 3000
        resp = self.client.post('/shorten', json={'original_url': very_long})
        self.assertEqual(resp.status_code, 400)

    @patch('URLTesting.app.get_db', create=True)
    def test_shorten_url_already_exist_redirect(self, mock_get_db):
        mock_collection = Mock()
        # 模擬有在urls 集合中找到 original value
        mock_collection.find_one.return_value = {
            "original_url": "https://stackoverflow.com/questions/77653645/preparing-metadata-setup-py-error-error-subprocess-exited-with-error",
            "short_url": "re4sNI"
        }
        # /re4sNI 應該會 redirect 到 original_url
        response = self.client.get('/re4sNI', follow_redirects=False)
        self.assertEqual(response.status_code, 302)

    @patch('URLTesting.app.get_db', create=True)
    def test_original_empty(self, mock_get_db):
        """original 為空值 → 400"""
        mock_collection = Mock()
        mock_get_db.return_value = mock_collection

        response = self.client.post('/shorten', json={'original_url': ""})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
