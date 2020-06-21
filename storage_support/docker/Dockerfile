FROM python:3.8.3-buster

COPY storage_support/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY storage_support/src/ /app/
WORKDIR /app/
