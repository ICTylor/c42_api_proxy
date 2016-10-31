"""
Tests for c42_proxy.py
"""
import unittest
import time
import c42_proxy

EVENT_ID = "b5ee7e41f16a4a62429655c619a5b5be_14770730026240"

class TestC42Proxy(unittest.TestCase):
    """
    Testing c42_proxy
    """
    def setUp(self):
        """
        Setups the flask application for testing
        """
        # creates a test client
        self.app = c42_proxy.app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        self.cache = c42_proxy.cache

    def tearDown(self):
        """
        Clears app and cache on teardown.
        """
        self.app = None
        self.cache = None

    def test_incorrect_route(self):
        """
        Tests incorrect route, should return a json error and status 404.
        """
        expected_json = b'{"error":{"status_code":404,"message":"Wrong endpoint"}}'
        response = self.app.get('/inexistent-endpoint')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_json)

    def test_incorrect_verb(self):
        """
        Tests incorrect verb, should return a json error and status 404.
        """
        expected_json = b'{"error":{"status_code":404,"message":"Wrong endpoint"}}'
        response = self.app.put('/events-with-subscriptions/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_json)
        response = self.app.delete('/events-with-subscriptions/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_json)
        response = self.app.post('/events-with-subscriptions/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data, expected_json)

    def test_valid_event(self):
        """
        Tests the correct response from the API.
        """
        expected_json = b'{"id":"b5ee7e41f16a4a62429655c619a5b5be_14770730026240","title":"Drink a cup of coffee with C42 Team","names":["API","Michel","Jasper","Bob","Dennis","Edmon","Aslesha","Lars"]}'
        response = self.app.get('/events-with-subscriptions/{}'.format(EVENT_ID))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_json)

    def test_cache(self):
        """
        Tests the cache is working correctly.
        """
        self.assertIsNone(self.cache.get(EVENT_ID))
        expected_json = b'{"id":"b5ee7e41f16a4a62429655c619a5b5be_14770730026240","title":"Drink a cup of coffee with C42 Team","names":["API","Michel","Jasper","Bob","Dennis","Edmon","Aslesha","Lars"]}'
        response = self.app.get('/events-with-subscriptions/{}'.format(EVENT_ID))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_json)
        self.assertIsNotNone(self.cache.get(EVENT_ID))
        response = self.app.get('/events-with-subscriptions/{}'.format(EVENT_ID))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected_json)
        self.assertIsNotNone(self.cache.get(EVENT_ID))
        time.sleep(1)
        self.assertIsNotNone(self.cache.get(EVENT_ID))
        time.sleep(4.2*60)
        self.assertIsNone(self.cache.get(EVENT_ID))

if __name__ == '__main__':
    unittest.main()
