FROM python:3.7

LABEL maintainer="marko.tuononen@gmail.com"

ADD requirements.list /tmp/requirements.list
RUN pip install -r /tmp/requirements.list

RUN useradd --create-home appuser
USER appuser

ADD app.py const.py labels.json /home/appuser/

WORKDIR /home/appuser
