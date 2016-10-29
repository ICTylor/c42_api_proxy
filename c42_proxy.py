"""
Provides a caching proxy for C42 events and subscriptions
"""
from flask import Flask, Response
from c42_requests import get_events_with_subscriptions_as_json
app = Flask(__name__)

# /events-with-subscriptions/$EVENT_ID/
@app.route("/events-with-subscriptions/<event_id>", methods=['GET'])
def events_with_subscriptions(event_id):
    """
    Exposes an endpoint that returns combined data from events and subscriptions.
    """
    result_json = get_events_with_subscriptions_as_json(event_id)
    response = Response(response=result_json, status=200, mimetype='application/json')
    return response

if __name__ == "__main__":
    app.run()
