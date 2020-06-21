FROM python:3.8.3-buster

COPY back/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY back/src/ /app/
WORKDIR /app/
