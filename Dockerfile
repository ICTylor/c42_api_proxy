FROM debian:stable

RUN apt-get update \
	&& apt-get install --no-install-recommends --no-install-suggests -y \
						python3-pip \
&& rm -rf /var/lib/apt/lists/*
COPY requirements.txt /requirements.txt
COPY *.py /
RUN pip3 install gunicorn && pip3 install -r requirements.txt
CMD ["gunicorn","-b","0.0.0.0:4242","c42_proxy:app"]
EXPOSE 4242