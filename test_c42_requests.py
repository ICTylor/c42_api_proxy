"""
Tests for c42_requests.py
"""
import unittest
from c42_requests import C42RequestsAPI

class TestRequestsOutput(unittest.TestCase):
    """
    Testing events with subscription
    """
    def test_correct_combined_output(self):
        """
        Test correct json output from get_events_with_subscriptions_as_json
        """
        event_id = "b5ee7e41f16a4a62429655c619a5b5be_14770730026240"
        c42_api = C42RequestsAPI()
        json_response = c42_api.get_events_with_subscriptions_as_json(event_id)
        expected_json = '{"id":"b5ee7e41f16a4a62429655c619a5b5be_14770730026240","title":"Drink a cup of coffee with C42 Team","names":["API","Michel","Jasper","Bob","Dennis","Edmon","Aslesha","Lars"]}'
        self.assertEqual(json_response, expected_json)

if __name__ == '__main__':
    unittest.main()
