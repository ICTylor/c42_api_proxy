"""
Provides a caching proxy for C42 events and subscriptions
"""
from werkzeug.contrib.cache import SimpleCache
from flask import Flask, Response
from c42_requests import C42RequestsAPI
app = Flask(__name__)
# Setting a default timeout of 4.2 minutes for the cache
cache = SimpleCache(default_timeout=int(4.2*60))
c42_api = C42RequestsAPI()

# /events-with-subscriptions/$EVENT_ID/
@app.route("/events-with-subscriptions/<event_id>", methods=['GET'])
def events_with_subscriptions(event_id):
    """
    Exposes an endpoint that returns combined data from events and subscriptions.
    """
    result_json = cache.get(event_id)
    if not result_json:
        result_json = c42_api.get_events_with_subscriptions_as_json(event_id)
        cache.set(event_id, result_json)
    response = Response(response=result_json, status=200, mimetype='application/json')
    return response

@app.errorhandler(404)
def wrong_endpoint(error):
    """
    Handles requests to a wrong url.
    Return a json error message and status code 404.
    """
    error_json = '{"error":{"status_code":404,"message":"Wrong endpoint"}}'
    response = Response(response=error_json, status=404, mimetype='application/json')
    return response

if __name__ == "__main__":
    app.run()
