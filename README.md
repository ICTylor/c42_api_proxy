# API framework

The first thing that comes to my mind when exposing HTTP endpoints in Python is Flask. Django is nice but it is a batteries included solution which I think is a bit overkill for the assignment. 
Also I am more familiar with Flask than with Django :)

Depending on the volume of petitions to the API per proxy server a different solution would probably be needed. Flask should be faster than Django, but still not very fast compared to other options. Flask is based on the Werkzeug WSGI library,
using Werkzeug directly will be faster. Another Python option is Falcon.
Other possible options to consider would be trying Go, Elixir/Erlang, custom C++ application, etc.

For the assignment I will keep it simple and use **Flask**.

Flask provides a builtin server which is useful for development and testing but should not be used in production. I will use **gunicorn** as the WSGI server. Another option would be using uWSGI but I will choose gunicorn as it is easier to configure.

To do the requests I will use the **requests** Python library.

JSON parsing will be achieved by using Python standard library **json** module.

Combination of the results should be straightforward.

# Caching

To cache the requests there are different options:
* Use a library that offers caching for Flask. Flask-Cache offers several options for caching, from simple dictionary caches to memcached support.
* Use **Werkzeug cache libraries directly**.
* Cache API requests by using a reverse proxy. For example use **Nginx** caching capabilities. In this case it is even possible to use a cache internal to the API Proxy and another one provided by the reverse proxy.

# Testing

Regarding testing I will first capture the requirements:

* The API proxy must respond to requests at /events-with-subscriptions/$EVENT_ID/
    * Routing should be tested to ensure that this is the only url exposed.
    * If a request is not correct or if there is a problem in the server it should either return an error response or nothing (it is not specified).
* The API proxy should return the right combined response
* The API proxy must cache the requests for 4.2 minutes(this might be tested using a smaller amount of time for the test)
    * If a request for a $EVENT_ID was made in the last 4.2 minutes it should not hit the C42 API.
    * If the last request for a $EVENT_ID was made in more than 4.2 minutes or never made it should hit the C42 API.

There are many libraries and frameworks for testing in Python. The most used is probably unittest as it is part of the standard library. Another interesting option is Behave which is based on Cucumber.
To keep things simple I will use **unittest**.

# Deployment

Both nginx and gunicorn require some configuration. I will provide a docker-compose.yml and Dockerfiles to make it easier to demonstrate a possible working configuration using **docker**.

# Running the server

Running using Flask development server directly:
```
python c42_proxy.py
```

Doing this will expose a Flask server on localhost:5000

Another option is running gunicorn with:
```
docker build -t ictylor/gunicorn
docker run --name test_gunicorn -p 80:4242 -t ictylor/gunicorn
```
Doing this will run a docker container and connect the internal port 4242 to external port 80

The last option is:
```
docker-compose build
docker-compose up
```
This option runs a container with nginx working as a reverse proxy for a gunicorn container.

# Testing instructions

Run all the tests with:
```
python -m unittest discover
```
Testing takes a long time because a test case waits for 4.2 minutes to test the cache.