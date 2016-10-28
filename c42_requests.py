"""
Provides an interface to C42 API (only GET events and GET event-subscriptions)
"""
import urllib
import json
from collections import OrderedDict
import requests

TOKEN = "b5c671777aa9372a79bcdb170437d0b5465ee4c2"
EVENT_ID = "b5ee7e41f16a4a62429655c619a5b5be_14770730026240"
HEADERS = {'Accept':'application/json', 'Content-type':'application/json',
           'Authorization':'Token {}'.format(TOKEN)}
# Timeout in seconds for requests
TIMEOUT = 4

def get_decoded_json_from_endpoint(endpoint, resource=None, params=None):
    """
    Requests information from a rest endpoint using GET.
    The url is completed with elements from params.
    Expects the response to be JSON.
    Returns an object with the information or None if there is an error.
    """
    try:
        url = urllib.parse.urljoin(endpoint, resource)
        response = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)
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

def get_event(event_id):
    """
    Requests information about an event identified by event_id using the C42 API.
    Returns an object with the information or None if there is an error.
    """
    endpoint = "https://demo.calendar42.com/api/v2/events/"
    resource = event_id
    return get_decoded_json_from_endpoint(endpoint, resource)

def get_event_subscriptions(event_id):
    """
    Requests information about users subscribed to an event identified by event_id using the C42 API.
    Returns an object with the information or None if there is an error.
    """
    endpoint = "https://demo.calendar42.com/api/v2/event-subscriptions/"
    params = {'event_ids':"[{}]".format(event_id)}
    return get_decoded_json_from_endpoint(endpoint, params=params)

def get_events_with_subscriptions(event_id):
    """
    Combines event data with subscription data.
    Returns a dictionary with the information or None if there is an error.
    """
    event = get_event(event_id)
    subscriptions = get_event_subscriptions(event_id)
    if event and subscriptions:
        # OrderedDict for consistent ordering of the keys
        combined = OrderedDict()
        combined['id'] = event_id
        combined['title'] = event['data'][0]['title']
        combined['names'] = [data['subscriber']['first_name'] for data in subscriptions['data']]
        return combined
    print('Event or subscriptions API failed, cannot return combined result')
    return None

def get_events_with_subscriptions_as_json(event_id):
    """
    Returns combined data from events and subscriptions as json or None if there is an error.
    """
    events_with_subscriptions_data = get_events_with_subscriptions(event_id)
    if events_with_subscriptions_data is None:
        return None
    return json.dumps(events_with_subscriptions_data)

def main():
    """
    Prints the combined result of event and subscription for the provided EVENT_ID
    """
    combined_json = get_events_with_subscriptions_as_json(EVENT_ID)
    print(combined_json)

if __name__ == '__main__':
    main()
