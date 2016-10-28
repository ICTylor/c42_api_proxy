"""
Provides an interface to C42 API (only GET events and GET event-subscriptions)
"""
import urllib
import json
import requests

TOKEN = "b5c671777aa9372a79bcdb170437d0b5465ee4c2"
EVENT_ID = "b5ee7e41f16a4a62429655c619a5b5be_14770730026240"
HEADERS = {'Accept':'application/json', 'Content-type':'application/json',
           'Authorization':'Token {}'.format(TOKEN)}

def get_event(event_id):
    """
    Requests information about an event identified by event_id using the C42 API.
    Returns an object with the information.
    """
    url = "https://demo.calendar42.com/api/v2/events/{}".format(event_id)
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_event_subscriptions(event_id):
    """
    Requests information about users subscribed to an event identified by event_id using the C42 API.
    Returns an object with the information.
    """
    url = "https://demo.calendar42.com/api/v2/event-subscriptions/?event_ids=[{}]".format(event_id)
    response = requests.get(url, headers=HEADERS)
    return response.json()

def get_events_with_subscriptions(event_id):
    """
    Combines event data with subscription data.
    Returns a dictionary with the information.
    """
    event = get_event(event_id)
    subscriptions = get_event_subscriptions(event_id)
    combined = {}
    combined['id'] = event_id
    combined['title'] = event['data'][0]['title']
    combined['names'] = [data['subscriber']['first_name'] for data in subscriptions['data']]
    return combined

def get_events_with_subscriptions_as_json(event_id):
    """
    Returns combined data from events and subscriptions as json or None if there is an error.
    """
    events_with_subscriptions_data = get_events_with_subscriptions(event_id)
    return json.dumps(events_with_subscriptions_data)

def main():
    """
    Prints the combined result of event and subscription for the provided EVENT_ID
    """
    combined_json = get_events_with_subscriptions_as_json(EVENT_ID)
    print(combined_json)

if __name__ == '__main__':
    main()
