FROM python:3.7-slim

COPY . /

RUN	apt-get update \
    && apt-get install -y build-essential \
    && pip3 install -r /requirements.txt \
    && apt-get purge -y build-essential \
    && apt-get autoremove -y \
    && apt-get clean