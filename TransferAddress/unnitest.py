import unittest
from app import app
from pymongo import MongoClient


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["shortener_db"]
        self.collection = self.db["urls"]

    def test_shorten_url_no_data(self):
        response = self.app.post('/shorten', json={})  # no url for testing
        self.assertEqual(response.status_code, 400)  # check is it 400, that is what we expected
        self.assertIn(b"No URL provided", response.data)  # if error 400 we raise No URL info

    def test_get_short_url_wrong_data(self):
        response = self.app.get('/wxyz12')
        self.assertEqual(response.status_code, 404)  # check is it 404, that is what we expected
        self.assertIn(b"URL not found", response.data)

    def test_shorten_url_already_exist(self):
        self.collection.insert_one({
            "original_url": "https://stackoverflow.com/questions/77653645/preparing-metadata-setup-py-error-error-subprocess-exited-with-error"},
            {"short_url": "re4sNI"})
        response = self.app.get('/re4sNI')
        self.assertEqual(response.status_code, 302)

    def test_get_short_url_post_data(self):
        response = self.app.post('/wxyz12')
        self.assertEqual(response.status_code, 405)  # check is it 404, that is what we expected

    def test_original_url_toolong(self):
        testing_url = "https://stackoverflow.com/questions/77653645/preparing-metadata-setup-py-error-error-subprocess-exited-with-error" + "abc1231312312fjwiof" * 2500
        if len(testing_url) > 2000:
            response = self.app.post('/shorten', json={'original_url': testing_url})
            self.assertEqual(response.status_code, 400)

    def test_original_no_data(self):
        response = self.app.post('/original', data={'original': ""})
        self.assertEqual(response.status_code, 400)

    def test_original_get(self):
        response = self.app.get('/original', data={'original': ""})
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
