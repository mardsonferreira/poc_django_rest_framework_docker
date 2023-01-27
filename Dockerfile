FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /poc_docker_python

WORKDIR /poc_docker_python

ADD . /poc_docker_python/

RUN pip install -r requirements.txt