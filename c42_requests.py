"""
Provides an interface to C42 API (only GET events and GET event-subscriptions)
"""
import concurrent.futures
import urllib
import json
from collections import OrderedDict
import requests

# The auth token should not be here, it should be passed
# as an argument or as an environment variable. But as
# it is a demo auth token and simplifies testing I think
# it is reasonable in this case.
TOKEN = "b5c671777aa9372a79bcdb170437d0b5465ee4c2"
EVENT_ID = "b5ee7e41f16a4a62429655c619a5b5be_14770730026240"

class C42RequestsAPI:
    """
    Exposes methods for requesting and combining information from C42 API.
    Needs a token for authorization. Timeout specifies a timeout for the
    requests.
    """
    def __init__(self, token=TOKEN, timeout=4):
        self._token = token
        self.timeout = timeout
        self.headers = {'Accept':'application/json', 'Content-type':'application/json',
                        'Authorization':'Token {}'.format(self.token)}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    @property
    def token(self):
        return self._token

    @token.setter
    def set_token(self, token):
        self._token = token
        self.headers = {'Accept':'application/json', 'Content-type':'application/json',
                        'Authorization':'Token {}'.format(self.token)}

    def get_decoded_json_from_endpoint(self, endpoint, resource=None, params=None):
        """
        Requests information from a rest endpoint using GET.
        The url is completed with elements from params.
        Expects the response to be JSON.
        Returns an object with the information or None if there is an error.
        """
        try:
            url = urllib.parse.urljoin(endpoint, resource)
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            return None
        except requests.exceptions.Timeout as err:
            # Maybe retry a configurable number of times
            print(err)
            return None
        except requests.exceptions.TooManyRedirects as err:
            print(err)
            print('Wrong url for endpoint')
            return None
        except requests.exceptions.RequestException as err:
            print(err)
            print('Something went wrong requesting data from endpoint')
            return None
        try:
            # Seems like requests has a .json() function, no need for json.loads()
            result = response.json()
        except ValueError as err:
            print(err)
            print('Something went wrong decoding json from endpoint')
        return result

    def get_event(self, event_id):
        """
        Requests information about an event identified by event_id using the C42 API.
        Returns an object with the information or None if there is an error.
        """
        endpoint = "https://demo.calendar42.com/api/v2/events/"
        resource = event_id
        return self.get_decoded_json_from_endpoint(endpoint, resource)

    def get_event_subscriptions(self, event_id):
        """
        Requests information about users subscribed to an event identified by event_id using the C42 API.
        Returns an object with the information or None if there is an error.
        """
        endpoint = "https://demo.calendar42.com/api/v2/event-subscriptions/"
        params = {'event_ids':"[{}]".format(event_id)}
        return self.get_decoded_json_from_endpoint(endpoint, params=params)

    def get_events_with_subscriptions(self, event_id):
        """
        Combines event data with subscription data.
        Returns a dictionary with the information or None if there is an error.
        """
        # Both API calls should be done asynchronously, otherwise we are wasting time
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_event = executor.submit(self.get_event, event_id)
            future_subscriptions = executor.submit(self.get_event_subscriptions, event_id)
            both_futures = [future_event, future_subscriptions]
            # Wait for both futures to complete
            concurrent.futures.wait(both_futures)
            event = future_event.result()
            subscriptions = future_subscriptions.result()
            if event and subscriptions:
                # OrderedDict for consistent ordering of the keys
                combined = OrderedDict()
                combined['id'] = event_id
                combined['title'] = event['data'][0]['title']
                combined['names'] = [data['subscriber']['first_name'] for data in subscriptions['data']]
                return combined
        print('Event or subscriptions API failed, cannot return combined result')
        return None

    def get_events_with_subscriptions_as_json(self, event_id):
        """
        Returns combined data from events and subscriptions as json or None if there is an error.
        """
        events_with_subscriptions_data = self.get_events_with_subscriptions(event_id)
        if events_with_subscriptions_data is None:
            return None
        # The json standard library provides some options to control the output style.
        # A compact representation can be achieved by setting the separators
        # argument. This saves some bytes when sending over HTTP
        return json.dumps(events_with_subscriptions_data, separators=(',', ':'))

    def __del__(self):
        self.session.close()

def main():
    """
    Prints the combined result of event and subscription for the provided EVENT_ID
    """
    c42_api = C42RequestsAPI()
    combined_json = c42_api.get_events_with_subscriptions_as_json(EVENT_ID)
    print(combined_json)

if __name__ == '__main__':
    main()
